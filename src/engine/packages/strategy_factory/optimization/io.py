"""Load V2 plan specifications from JSON or optional YAML."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


def load_plan_spec(path: str | Path) -> Mapping[str, Any]:
    resolved = Path(path).expanduser().resolve()
    suffix = resolved.suffix.lower()
    text = resolved.read_text(encoding="utf-8")
    if suffix == ".json":
        value = json.loads(text)
    elif suffix in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise RuntimeError("PyYAML is required to load YAML plan specifications") from exc
        value = yaml.safe_load(text)
    else:
        raise ValueError(f"unsupported plan format: {suffix}")
    if not isinstance(value, Mapping):
        raise ValueError("plan specification root must be an object")
    return value
