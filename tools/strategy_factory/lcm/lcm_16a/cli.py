from __future__ import annotations

import argparse
import json
from pathlib import Path

from .patch_verify import verify_hash_ledger
from .qa import run_qa
from .schema_validation import validate_schemas
from .static_validation import static_validate
from .verify import verify_package


def main() -> int:
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(dest="command", required=True)

    command = subcommands.add_parser("verify-patch")
    command.add_argument("--repo-root", required=True)
    command.add_argument("--hash-ledger", required=True)

    command = subcommands.add_parser("validate-schemas")
    command.add_argument("--schema-root", required=True)

    command = subcommands.add_parser("static-validate")
    command.add_argument("--module-root", required=True)

    command = subcommands.add_parser("verify-package")
    command.add_argument("--repo-root", default=".")
    command.add_argument("--audit-root", required=True)

    command = subcommands.add_parser("qa")
    command.add_argument("--repo-root", default=".")
    command.add_argument("--audit-root", required=True)
    command.add_argument("--schema-root", required=True)
    command.add_argument("--module-root", required=True)

    args = parser.parse_args()
    if args.command == "verify-patch":
        output = {
            "verified_file_count": verify_hash_ledger(
                Path(args.repo_root), Path(args.hash_ledger)
            ),
            "validation_status": "PASS",
        }
    elif args.command == "validate-schemas":
        output = {
            "schema_count": validate_schemas(Path(args.schema_root)),
            "validation_status": "PASS",
        }
    elif args.command == "static-validate":
        output = {
            "module_count": static_validate(Path(args.module_root)),
            "validation_status": "PASS",
        }
    elif args.command == "verify-package":
        output = verify_package(Path(args.repo_root), Path(args.audit_root)).__dict__
    else:
        output = run_qa(
            Path(args.repo_root),
            Path(args.audit_root),
            Path(args.schema_root),
            Path(args.module_root),
        )
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
