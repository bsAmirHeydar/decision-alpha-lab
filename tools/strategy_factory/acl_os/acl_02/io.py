from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import yaml
from .errors import PackageLoadError

def load_structured(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".json":
            return json.loads(text)
        if path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(text)
        return text
    except Exception as exc:
        raise PackageLoadError(f"cannot load {path}: {exc}") from exc

def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def load_yaml(path: Path) -> dict:
    obj = load_structured(path)
    if not isinstance(obj, dict):
        raise PackageLoadError(f"expected mapping: {path}")
    return obj
