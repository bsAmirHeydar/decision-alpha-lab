from __future__ import annotations

import json
from pathlib import Path

import yaml

from .canonical import normalize_root_relative


def validate_registry_tree(registry_root: Path) -> dict:
    json_count = 0
    yaml_count = 0
    for path in registry_root.rglob("*"):
        if not path.is_file():
            continue
        normalize_root_relative(path.relative_to(registry_root).as_posix())
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
        elif path.suffix in {".yaml", ".yml"}:
            yaml.safe_load(path.read_text(encoding="utf-8"))
            yaml_count += 1
    return {"passed": True, "json_count": json_count, "yaml_count": yaml_count}
