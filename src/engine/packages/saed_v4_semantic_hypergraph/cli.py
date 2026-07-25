from __future__ import annotations

import argparse
import json
from pathlib import Path

from .catalog import institutional_policy, institutional_registry
from .contracts import load_json
from .serialization import to_document, write_json


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="saed-v4-hypergraph")
    sub = parser.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("inspect-registry", help="Print the immutable institutional registry and policy.")
    inspect.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "inspect-registry":
        payload = {
            "registry": to_document(institutional_registry()),
            "policy": to_document(institutional_policy()),
        }
        if args.output:
            write_json(args.output, payload)
        else:
            print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
