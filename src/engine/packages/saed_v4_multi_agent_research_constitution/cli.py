from __future__ import annotations
import argparse
import json
from pathlib import Path
from .service import run

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="SAED V4-32 deterministic multi-agent research constitution reference")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = run(json.loads(args.input.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
