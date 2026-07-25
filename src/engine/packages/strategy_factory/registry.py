"""Versioned registries for strategies, policies, models, and runs."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence
import json


@dataclass(frozen=True)
class RegistryEntry:
    object_id: str
    object_type: str
    version: str
    status: str
    artifact_path: str
    artifact_hash: str
    metadata: Mapping[str, Any]


class JsonRegistry:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._entries: Dict[str, RegistryEntry] = {}
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            for item in raw.get("entries", []):
                entry = RegistryEntry(**item)
                self._entries[entry.object_id] = entry

    def add(self, entry: RegistryEntry, *, allow_new_version: bool = True) -> None:
        existing = self._entries.get(entry.object_id)
        if existing is not None and existing.version == entry.version:
            raise ValueError(f"registry entry already exists: {entry.object_id}@{entry.version}")
        if existing is not None and not allow_new_version:
            raise ValueError(f"registry object already exists: {entry.object_id}")
        self._entries[entry.object_id] = entry

    def get(self, object_id: str) -> Optional[RegistryEntry]:
        return self._entries.get(object_id)

    def entries(self, object_type: Optional[str] = None) -> Sequence[RegistryEntry]:
        values = tuple(self._entries.values())
        if object_type is None:
            return values
        return tuple(item for item in values if item.object_type == object_type)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema_version": "1.0.0", "entries": [asdict(item) for item in self._entries.values()]}
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
