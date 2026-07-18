from __future__ import annotations
from pathlib import Path
from typing import Any
from .canonical import canonical_bytes, digest_bytes, stable_id, with_digest
from .errors import CacheError

class RunArtifactStore:
    def __init__(self, root: Path):
        self.root = root
        self.records: list[dict[str, Any]] = []
        (root / "objects/sha256").mkdir(parents=True, exist_ok=True)

    def put(self, logical_id: str, artifact_class: str, value: Any, source_task_id: str) -> dict[str, Any]:
        payload = canonical_bytes(value) + b"\n"
        blob = digest_bytes(payload)
        hx = blob.split(":", 1)[1]
        rel = f"objects/sha256/{hx[:2]}/{hx[2:]}.json"
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_bytes() != payload:
            raise CacheError("digest collision or mutable object")
        if not path.exists():
            path.write_bytes(payload)
        body = {
            "schema_version": "1.0.0",
            "object_id": stable_id("RUNOBJ", blob, length=24),
            "logical_id": logical_id,
            "artifact_class": artifact_class,
            "blob_digest": blob,
            "size_bytes": len(payload),
            "store_path": rel,
            "source_task_id": source_task_id,
            "immutable": True,
        }
        record = with_digest(body, "record_digest")
        self.records.append(record)
        return record

    def index(self) -> dict[str, Any]:
        unique = {r["record_digest"]: r for r in self.records}
        records = sorted(unique.values(), key=lambda r: (r["artifact_class"], r["logical_id"], r["record_digest"]))
        return with_digest(
            {
                "schema_version": "1.0.0",
                "objects": records,
                "object_count": len(records),
                "total_bytes": sum(r["size_bytes"] for r in records),
                "content_addressed": True,
                "mutable": False,
            },
            "object_index_digest",
        )
