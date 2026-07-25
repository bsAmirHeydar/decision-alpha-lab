from __future__ import annotations

import argparse
import json
from pathlib import Path

from .conformance import run_conformance
from .golden import golden_vector_material


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FP-I02 core contract kernel")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("conformance")
    vector = sub.add_parser("vectors")
    vector.add_argument("--output")
    args = parser.parse_args(argv)
    if args.command == "conformance":
        report = run_conformance()
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["passed"] else 1
    material = golden_vector_material()
    text = json.dumps(material, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
