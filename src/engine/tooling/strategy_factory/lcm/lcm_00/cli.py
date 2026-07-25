from __future__ import annotations

import argparse
import json
from pathlib import Path

from .service import FreezeConfig, freeze_repository
from .verify import verify_baseline_package, verify_repository_against_baseline


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lcm-00")
    sub = parser.add_subparsers(dest="command", required=True)

    verify = sub.add_parser("verify-package")
    verify.add_argument("--package-root", type=Path, required=True)

    install = sub.add_parser("verify-installation")
    install.add_argument("--repo-root", type=Path, required=True)
    install.add_argument("--package-root", type=Path, required=True)
    install.add_argument("--allowed-additions-file", type=Path, required=True)

    freeze = sub.add_parser("freeze")
    freeze.add_argument("--source-root", type=Path, required=True)
    freeze.add_argument("--destination", type=Path, required=True)
    freeze.add_argument("--rehearsal-root", type=Path, required=True)
    freeze.add_argument("--ownership-registry", type=Path, required=True)
    freeze.add_argument("--source-program-digest", required=True)
    freeze.add_argument("--issued-at", required=True)

    args = parser.parse_args(argv)
    if args.command == "verify-package":
        result = verify_baseline_package(args.package_root)
    elif args.command == "verify-installation":
        additions = {line.strip().replace("\\", "/") for line in args.allowed_additions_file.read_text(encoding="utf-8").splitlines() if line.strip()}
        result = verify_repository_against_baseline(args.repo_root, args.package_root, additions)
    else:
        result_path = freeze_repository(FreezeConfig(
            source_root=args.source_root,
            destination=args.destination,
            rehearsal_root=args.rehearsal_root,
            issued_at=args.issued_at,
            source_program_digest=args.source_program_digest,
            ownership_registry=_load(args.ownership_registry),
        ))
        result = {"passed": True, "destination": str(result_path)}
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
