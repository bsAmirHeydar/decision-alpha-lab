"""Command-line entry points for UCE-I11 validation and golden compilation."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .canonical import canonical_json
from .compiler import ExperimentDagCompiler
from .conformance import generate_vectors, verify_vectors
from .golden import golden_declaration


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="strategy-factory-experiments-v3")
    sub = parser.add_subparsers(dest="command", required=True)
    compile_parser = sub.add_parser("compile-golden")
    compile_parser.add_argument("--output", type=Path)
    vector_parser = sub.add_parser("generate-vectors")
    vector_parser.add_argument("--output", type=Path, required=True)
    verify_parser = sub.add_parser("verify-vectors")
    verify_parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)

    if args.command == "compile-golden":
        manifest = ExperimentDagCompiler().compile(golden_declaration())
        text = canonical_json(asdict(manifest))
        if args.output:
            args.output.write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 0
    if args.command == "generate-vectors":
        args.output.write_text(json.dumps(generate_vectors(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return 0
    if args.command == "verify-vectors":
        vectors = json.loads(args.path.read_text(encoding="utf-8"))
        if not verify_vectors(vectors):
            raise SystemExit("conformance vectors do not match")
        print("UCE-I11 conformance vectors: PASS")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
