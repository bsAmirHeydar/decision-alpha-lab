from __future__ import annotations

import argparse
import json
from pathlib import Path

from .build import build_program_closure_package
from .closure import evaluate_program_closure
from .evidence import validate_external_evidence_bundle
from .io import load_json, write_json
from .patch_verify import verify_hash_ledger
from .qa import run_qa
from .schema_validation import validate_schemas
from .static_validation import static_validate
from .verify import verify_program_closure_package


def main() -> int:
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(dest="command", required=True)

    command = subcommands.add_parser("build")
    command.add_argument("--repo-root", default=".")
    command.add_argument("--package-root")

    command = subcommands.add_parser("verify-patch")
    command.add_argument("--repo-root", required=True)
    command.add_argument("--hash-ledger", required=True)

    command = subcommands.add_parser("validate-schemas")
    command.add_argument("--schema-root", required=True)

    command = subcommands.add_parser("static-validate")
    command.add_argument("--module-root", required=True)

    command = subcommands.add_parser("verify-package")
    command.add_argument("--repo-root", default=".")
    command.add_argument("--closure-root", required=True)

    command = subcommands.add_parser("qa")
    command.add_argument("--repo-root", default=".")
    command.add_argument("--closure-root", required=True)
    command.add_argument("--schema-root", required=True)
    command.add_argument("--module-root", required=True)

    command = subcommands.add_parser("evaluate-evidence")
    command.add_argument("--repo-root", default=".")
    command.add_argument("--closure-root", required=True)
    command.add_argument("--evidence-root", required=True)
    command.add_argument("--bundle", required=True)
    command.add_argument("--output-dir", required=True)

    args = parser.parse_args()
    if args.command == "build":
        package = build_program_closure_package(
            Path(args.repo_root), Path(args.package_root) if args.package_root else None
        )
        output = {"package_root": str(package), "validation_status": "PASS"}
    elif args.command == "verify-patch":
        output = {
            "verified_file_count": verify_hash_ledger(Path(args.repo_root), Path(args.hash_ledger)),
            "validation_status": "PASS",
        }
    elif args.command == "validate-schemas":
        output = {"schema_count": validate_schemas(Path(args.schema_root)), "validation_status": "PASS"}
    elif args.command == "static-validate":
        output = {"module_count": static_validate(Path(args.module_root)), "validation_status": "PASS"}
    elif args.command == "verify-package":
        output = verify_program_closure_package(Path(args.repo_root), Path(args.closure_root)).__dict__
    elif args.command == "qa":
        output = run_qa(
            Path(args.repo_root), Path(args.closure_root), Path(args.schema_root), Path(args.module_root)
        )
    else:
        repo_root = Path(args.repo_root).resolve()
        closure_root = Path(args.closure_root).resolve()
        evidence = validate_external_evidence_bundle(
            repo_root, Path(args.evidence_root).resolve(), Path(args.bundle).resolve()
        )
        recovery = load_json(closure_root / "recovery_drill_receipt.json")
        decision, certificate = evaluate_program_closure(recovery, evidence)
        output_dir = Path(args.output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        write_json(output_dir / "validated_external_evidence_status.json", evidence)
        write_json(output_dir / "program_closure_decision.json", decision)
        write_json(output_dir / "program_closure_certificate.json", certificate)
        output = {
            "program_closure_decision": decision["decision"],
            "certificate_status": certificate["certificate_status"],
            "output_dir": str(output_dir),
            "validation_status": "PASS",
        }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
