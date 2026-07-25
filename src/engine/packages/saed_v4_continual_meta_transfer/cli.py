from __future__ import annotations

import argparse
import json
from pathlib import Path

from .service import run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SAED V4-25 continual meta and transfer reference runner")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--upstream", required=True, type=Path)
    parser.add_argument("--tasks", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    upstream = json.loads(args.upstream.read_text(encoding="utf-8"))
    tasks = json.loads(args.tasks.read_text(encoding="utf-8"))
    outputs = run(config, upstream, tasks)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, value in outputs.items():
        path = args.output / f"{name.upper()}.JSON"
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
