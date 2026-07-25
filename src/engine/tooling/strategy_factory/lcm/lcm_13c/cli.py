from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .patch_verify import verify_hash_ledger
from .qa import run_qa
from .schema_validation import validate_schema_directory
from .static_validation import static_validate
from .verify import verify_package


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    command = sub.add_parser("verify-patch")
    command.add_argument("--repo-root", required=True)
    command.add_argument("--hash-ledger", required=True)

    command = sub.add_parser("validate-schemas")
    command.add_argument("--schema-root", required=True)

    command = sub.add_parser("static-validate")
    command.add_argument("--module-root", required=True)

    command = sub.add_parser("verify-package")
    command.add_argument("--closure-root", required=True)

    command = sub.add_parser("verify-installation")
    command.add_argument("--repo-root", required=True)
    command.add_argument("--closure-root", required=True)
    command.add_argument("--patch-index", required=True)

    command = sub.add_parser("qa")
    command.add_argument("--closure-root", required=True)
    command.add_argument("--schema-root", required=True)
    command.add_argument("--module-root", required=True)

    args = parser.parse_args(argv)
    errors: list[str]
    if args.command == "verify-patch":
        errors = verify_hash_ledger(Path(args.repo_root), Path(args.hash_ledger))
    elif args.command == "validate-schemas":
        errors = validate_schema_directory(Path(args.schema_root))
    elif args.command == "static-validate":
        errors = static_validate(Path(args.module_root))
    elif args.command == "verify-package":
        errors = verify_package(Path(args.closure_root))
    elif args.command == "verify-installation":
        errors = verify_package(Path(args.closure_root))
        index = [
            line.strip()
            for line in Path(args.patch_index).read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        ]
        errors += [
            "INDEX_MISSING:" + relative
            for relative in index
            if not (Path(args.repo_root) / relative).is_file()
        ]
    else:
        errors = run_qa(
            Path(args.closure_root), Path(args.schema_root), Path(args.module_root)
        )
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
