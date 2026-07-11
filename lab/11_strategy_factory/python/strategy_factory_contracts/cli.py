from __future__ import annotations
import argparse, json
from pathlib import Path
from .registry import default_registry

def main() -> int:
    parser = argparse.ArgumentParser(description="Strategy Factory Phase 01 contract tools")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("registry")
    validate = sub.add_parser("validate-registry")
    validate.add_argument("path", type=Path)
    args = parser.parse_args()
    if args.command == "registry":
        print(json.dumps(default_registry().as_dict(), indent=2, sort_keys=True))
        return 0
    payload = json.loads(args.path.read_text(encoding="utf-8"))
    expected = default_registry().as_dict()
    actual = {item["name"]: f'{item["namespace"]}/{item["name"]}@{item["version"]}' for item in payload["schemas"]}
    if actual != expected:
        print(json.dumps({"status": "FAIL", "expected": expected, "actual": actual}, indent=2))
        return 1
    print(json.dumps({"status": "PASS", "schema_count": len(actual)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
