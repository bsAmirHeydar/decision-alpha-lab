"""Command-line interface for SAED V4-00 constitution validation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .canonical import content_hash
from .conformance import run_vector
from .contracts import load_document, load_schema, validate_closed
from .core_boundary import capture_snapshot, compare_snapshots
from .crosswalk import build_crosswalk
from .policy import ConstitutionKernel, ConstitutionPolicy


def _write(value: object, output: str | None) -> None:
    text = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def command_validate(args: argparse.Namespace) -> int:
    document = load_document(args.document)
    schema = load_schema(args.schema)
    validate_closed(document, schema)
    _write({"status": "pass", "document_hash": content_hash(document)}, args.output)
    return 0


def command_conformance(args: argparse.Namespace) -> int:
    vectors = load_document(args.vectors)
    constitution = load_document(args.constitution)
    kernel = ConstitutionKernel(content_hash(constitution), ConstitutionPolicy.default())
    results = [run_vector(kernel, v) for v in vectors["vectors"]]
    passed = sum(1 for x in results if x["matches_expected"])
    payload = {"status": "pass" if passed == len(results) else "fail", "passed": passed, "total": len(results), "results": results}
    _write(payload, args.output)
    return 0 if passed == len(results) else 2


def command_snapshot(args: argparse.Namespace) -> int:
    snapshot = capture_snapshot(args.root, patterns=args.pattern or None, exclude=args.exclude or ()) if args.pattern else capture_snapshot(args.root, exclude=args.exclude or ())
    _write(snapshot, args.output)
    return 0


def command_compare(args: argparse.Namespace) -> int:
    before = load_document(args.before)
    after = load_document(args.after)
    result = compare_snapshots(before, after)
    _write(result, args.output)
    return 0 if result["status"] == "allow" else 3


def command_crosswalk(args: argparse.Namespace) -> int:
    _write(build_crosswalk(), args.output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="saed-v4-constitution")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("--document", required=True)
    validate.add_argument("--schema", required=True)
    validate.add_argument("--output")
    validate.set_defaults(func=command_validate)

    conf = sub.add_parser("conformance")
    conf.add_argument("--constitution", required=True)
    conf.add_argument("--vectors", required=True)
    conf.add_argument("--output")
    conf.set_defaults(func=command_conformance)

    snap = sub.add_parser("snapshot-core")
    snap.add_argument("--root", required=True)
    snap.add_argument("--pattern", action="append")
    snap.add_argument("--exclude", action="append")
    snap.add_argument("--output")
    snap.set_defaults(func=command_snapshot)

    compare = sub.add_parser("compare-core")
    compare.add_argument("--before", required=True)
    compare.add_argument("--after", required=True)
    compare.add_argument("--output")
    compare.set_defaults(func=command_compare)

    cross = sub.add_parser("render-crosswalk")
    cross.add_argument("--output")
    cross.set_defaults(func=command_crosswalk)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
