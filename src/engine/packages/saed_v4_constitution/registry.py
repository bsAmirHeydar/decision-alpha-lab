"""Immutable exact-version registry for constitutions, policies and programs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import content_hash
from .errors import IntegrityViolation


@dataclass(frozen=True)
class RegistryRecord:
    artifact_type: str
    artifact_id: str
    version: str
    artifact_hash: str
    known_time: str
    status: str

    @property
    def key(self) -> tuple[str, str, str]:
        return self.artifact_type, self.artifact_id, self.version


class ExactVersionRegistry:
    def __init__(self) -> None:
        self._records: dict[tuple[str, str, str], RegistryRecord] = {}

    def register(self, record: RegistryRecord) -> None:
        prior = self._records.get(record.key)
        if prior and prior != record:
            raise IntegrityViolation(f"immutable registry key already exists with different content: {record.key}")
        self._records[record.key] = record

    def get(self, artifact_type: str, artifact_id: str, version: str) -> RegistryRecord:
        return self._records[(artifact_type, artifact_id, version)]

    def snapshot(self) -> dict[str, Any]:
        records = [r.__dict__ for r in sorted(self._records.values(), key=lambda x: x.key)]
        return {"records": records, "snapshot_hash": content_hash(records)}
