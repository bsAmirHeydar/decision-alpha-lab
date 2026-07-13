"""Content-addressed cache with strict provenance validation."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable, Mapping

from .canonical import bytes_sha256, canonical_json, canonical_sha256
from .contracts import CacheLookup, CacheRecord
from .enums import CacheStatus
from .errors import ExperimentError


class ContentAddressedCache:
    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root is not None else None
        self._records: dict[str, CacheRecord] = {}
        self._payloads: dict[str, bytes] = {}
        if self.root is not None:
            self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def key_for(
        *,
        namespace: str,
        artifact_kind: str,
        producer_version: str,
        schema_version: str,
        input_hashes: Iterable[str],
        provenance_hash: str,
    ) -> str:
        return canonical_sha256(
            {
                "namespace": namespace,
                "artifact_kind": artifact_kind,
                "producer_version": producer_version,
                "schema_version": schema_version,
                "input_hashes": tuple(input_hashes),
                "provenance_hash": provenance_hash,
            }
        )

    def put(
        self,
        *,
        namespace: str,
        artifact_kind: str,
        producer_version: str,
        schema_version: str,
        input_hashes: Iterable[str],
        provenance_hash: str,
        payload: bytes,
        created_sequence: int,
        metadata: Mapping[str, Any] | None = None,
    ) -> CacheRecord:
        inputs = tuple(input_hashes)
        key = self.key_for(
            namespace=namespace,
            artifact_kind=artifact_kind,
            producer_version=producer_version,
            schema_version=schema_version,
            input_hashes=inputs,
            provenance_hash=provenance_hash,
        )
        record = CacheRecord(
            cache_key=key,
            namespace=namespace,
            artifact_kind=artifact_kind,
            producer_version=producer_version,
            schema_version=schema_version,
            input_hashes=inputs,
            payload_hash=bytes_sha256(payload),
            provenance_hash=provenance_hash,
            created_sequence=created_sequence,
            size_bytes=len(payload),
            metadata=dict(metadata or {}),
        )
        self._records[key] = record
        self._payloads[key] = bytes(payload)
        if self.root is not None:
            directory = self.root / key[:2] / key
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "payload.bin").write_bytes(payload)
            (directory / "record.json").write_text(canonical_json(asdict(record)), encoding="utf-8")
        return record

    def _load_disk(self, key: str) -> None:
        if self.root is None or key in self._records:
            return
        directory = self.root / key[:2] / key
        record_path = directory / "record.json"
        payload_path = directory / "payload.bin"
        if not record_path.exists() or not payload_path.exists():
            return
        raw = json.loads(record_path.read_text(encoding="utf-8"))
        record = CacheRecord(
            cache_key=raw["cache_key"],
            namespace=raw["namespace"],
            artifact_kind=raw["artifact_kind"],
            producer_version=raw["producer_version"],
            schema_version=raw["schema_version"],
            input_hashes=tuple(raw["input_hashes"]),
            payload_hash=raw["payload_hash"],
            provenance_hash=raw["provenance_hash"],
            created_sequence=int(raw["created_sequence"]),
            size_bytes=int(raw["size_bytes"]),
            metadata=raw.get("metadata", {}),
        )
        self._records[key] = record
        self._payloads[key] = payload_path.read_bytes()

    def lookup(
        self,
        key: str,
        *,
        producer_version: str,
        schema_version: str,
        input_hashes: Iterable[str],
        provenance_hash: str,
    ) -> CacheLookup:
        self._load_disk(key)
        record = self._records.get(key)
        if record is None:
            return CacheLookup(key, CacheStatus.MISS, "cache_key_not_found", None)
        payload = self._payloads.get(key, b"")
        if bytes_sha256(payload) != record.payload_hash or len(payload) != record.size_bytes:
            return CacheLookup(key, CacheStatus.CORRUPT, "payload_integrity_mismatch", record)
        if record.producer_version != producer_version or record.schema_version != schema_version:
            return CacheLookup(key, CacheStatus.STALE, "producer_or_schema_version_changed", record)
        if record.input_hashes != tuple(input_hashes) or record.provenance_hash != provenance_hash:
            return CacheLookup(key, CacheStatus.INCOMPATIBLE, "input_or_provenance_mismatch", record)
        expected_key = self.key_for(
            namespace=record.namespace,
            artifact_kind=record.artifact_kind,
            producer_version=producer_version,
            schema_version=schema_version,
            input_hashes=input_hashes,
            provenance_hash=provenance_hash,
        )
        if expected_key != key:
            return CacheLookup(key, CacheStatus.INCOMPATIBLE, "cache_identity_mismatch", record)
        return CacheLookup(key, CacheStatus.VALID, "", record)

    def payload(self, key: str) -> bytes:
        self._load_disk(key)
        try:
            return self._payloads[key]
        except KeyError as exc:
            raise ExperimentError("cache_payload_missing", "cache payload is unavailable", {"key": key}) from exc

    def corrupt_for_test(self, key: str, payload: bytes) -> None:
        if key not in self._records:
            raise ExperimentError("cache_key_not_found", "cannot corrupt absent cache record")
        self._payloads[key] = payload
