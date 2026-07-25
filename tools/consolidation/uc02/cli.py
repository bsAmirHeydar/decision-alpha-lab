"""Command-line interface for UC-02 standards and authority freeze."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .constants import AUTHORITY_ROOT
from .generator import build_authority_package
from .guard import run_guard
from .qualification import finalize, qualify
from .verify import verify_authority_package, verify_static_patch


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="uc02", description="Alpha Lab UC-02 standards and authority freeze")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "qualify", "finalize", "verify"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--repo-root", default=".")
        cmd.add_argument("--authority-root")
    reference = sub.add_parser("reference-build")
    reference.add_argument("--repo-root", default=".")
    reference.add_argument("--authority-root", required=True)
    guard = sub.add_parser("guard")
    guard.add_argument("--repo-root", default=".")
    guard.add_argument("--require-authority-package", action="store_true")
    static = sub.add_parser("verify-static-patch")
    static.add_argument("--repo-root", default=".")
    run_all = sub.add_parser("run-all")
    run_all.add_argument("--repo-root", default=".")
    run_all.add_argument("--authority-root")
    return parser


def _roots(args: argparse.Namespace) -> tuple[Path, Path]:
    repo = Path(args.repo_root).resolve()
    authority_arg = getattr(args, "authority_root", None)
    authority = Path(authority_arg).resolve() if authority_arg else repo / AUTHORITY_ROOT
    return repo, authority


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    repo, authority = _roots(args)
    if args.command == "build":
        result = build_authority_package(repo, authority)
    elif args.command == "reference-build":
        result = build_authority_package(repo, authority, allow_reference=True)
    elif args.command == "qualify":
        result = qualify(repo, authority)
    elif args.command == "finalize":
        result = finalize(repo, authority)
    elif args.command == "verify":
        result = verify_authority_package(repo, authority)
    elif args.command == "guard":
        result = run_guard(repo, require_authority_package=args.require_authority_package)
    elif args.command == "verify-static-patch":
        result = verify_static_patch(repo)
    elif args.command == "run-all":
        result = {
            "build": build_authority_package(repo, authority),
            "qualify": qualify(repo, authority),
            "finalize": finalize(repo, authority),
            "verify": verify_authority_package(repo, authority),
        }
    else:  # pragma: no cover
        raise AssertionError(args.command)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if args.command == "run-all":
        return 0 if result["finalize"].get("status") == "ACCEPTED" and result["verify"].get("status") == "PASS" else 1
    return 0 if result.get("status") in {"PASS", "ACCEPTED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
