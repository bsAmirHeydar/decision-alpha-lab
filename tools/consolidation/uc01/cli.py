"""Command-line interface for UC-01 preservation and baseline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .capture import (
    assemble_baseline,
    capture_artifacts,
    capture_baseline,
    capture_documents_and_schemas,
    capture_mql5_surface,
    capture_path_references,
    capture_python_surface,
    finalize,
    preserve_baseline,
    qualify,
    resume_capture,
    run_recovery,
)
from .constants import BASELINE_RELATIVE_ROOT
from .verify import verify_baseline, verify_static_patch


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="uc01", description="Alpha Lab UC-01 preservation and baseline")
    sub = parser.add_subparsers(dest="command", required=True)

    def roots(command_parser: argparse.ArgumentParser) -> None:
        command_parser.add_argument("--repo-root", default=".")
        command_parser.add_argument("--baseline-root")

    capture = sub.add_parser("capture", help="Run all resumable capture steps")
    roots(capture)
    capture.add_argument("--allow-existing", action="store_true")

    resume = sub.add_parser("resume", help="Resume missing capture steps from capture_state.json")
    roots(resume)

    for name, help_text in (
        ("capture-artifacts", "Hash and classify every repository artifact"),
        ("capture-python", "Capture Python symbols, imports, parse issues and tests"),
        ("capture-mql5", "Capture MQL5 symbols, includes and authority surfaces"),
        ("capture-documents", "Capture documentation, links, note IDs and schemas"),
        ("capture-references", "Capture raw repository path references"),
        ("assemble", "Assemble consumers, critical logic, unresolved items and manifest"),
    ):
        roots(sub.add_parser(name, help=help_text))

    preserve = sub.add_parser("preserve", help="Create Git refs, Git bundle and external source archive")
    roots(preserve)
    preserve.add_argument("--preservation-root", required=True)
    preserve.add_argument("--overwrite-artifacts", action="store_true")

    recovery = sub.add_parser("recovery-drill", help="Restore external archive into isolation and compare every file")
    roots(recovery)

    qualification = sub.add_parser("qualify", help="Run UC-01 tests, Engineering Policy and optional full regression")
    roots(qualification)
    qualification.add_argument("--skip-full-regression", action="store_true")

    final = sub.add_parser("finalize", help="Evaluate non-compensatory gates and issue or withhold UC-02 handoff")
    roots(final)

    static_verify = sub.add_parser("verify-static-patch", help="Verify static patch index, hashes, manifest and inventory")
    static_verify.add_argument("--repo-root", default=".")

    verify = sub.add_parser("verify", help="Verify baseline files, hashes, authority and current-tree parity")
    roots(verify)
    verify.add_argument("--skip-current-tree", action="store_true")

    all_cmd = sub.add_parser("run-all", help="Capture, preserve, recover, qualify, finalize and verify")
    roots(all_cmd)
    all_cmd.add_argument("--preservation-root", required=True)
    all_cmd.add_argument("--overwrite-artifacts", action="store_true")
    all_cmd.add_argument("--skip-full-regression", action="store_true")
    return parser


def _roots(args: argparse.Namespace) -> tuple[Path, Path]:
    repo = Path(args.repo_root).resolve()
    baseline_arg = getattr(args, "baseline_root", None)
    baseline = Path(baseline_arg).resolve() if baseline_arg else repo / BASELINE_RELATIVE_ROOT
    return repo, baseline


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    repo, baseline = _roots(args)
    command = args.command
    if command == "verify-static-patch":
        result = verify_static_patch(repo)
    elif command == "capture":
        result = capture_baseline(repo, baseline, allow_existing=args.allow_existing)
    elif command == "resume":
        result = resume_capture(repo, baseline)
    elif command == "capture-artifacts":
        baseline.mkdir(parents=True, exist_ok=True)
        result = capture_artifacts(repo, baseline)
    elif command == "capture-python":
        result = capture_python_surface(repo, baseline)
    elif command == "capture-mql5":
        result = capture_mql5_surface(repo, baseline)
    elif command == "capture-documents":
        result = capture_documents_and_schemas(repo, baseline)
    elif command == "capture-references":
        result = capture_path_references(repo, baseline)
    elif command == "assemble":
        result = assemble_baseline(repo, baseline)
    elif command == "preserve":
        result = preserve_baseline(repo, baseline, Path(args.preservation_root).resolve(), overwrite_artifacts=args.overwrite_artifacts)
    elif command == "recovery-drill":
        result = run_recovery(baseline)
    elif command == "qualify":
        result = qualify(repo, baseline, include_full_regression=not args.skip_full_regression)
    elif command == "finalize":
        result = finalize(repo, baseline)
    elif command == "verify":
        result = verify_baseline(repo, baseline, verify_current_tree=not args.skip_current_tree)
    elif command == "run-all":
        results = {
            "capture": resume_capture(repo, baseline),
            "preserve": preserve_baseline(repo, baseline, Path(args.preservation_root).resolve(), overwrite_artifacts=args.overwrite_artifacts),
            "recovery": run_recovery(baseline),
            "qualification": qualify(repo, baseline, include_full_regression=not args.skip_full_regression),
            "finalize": finalize(repo, baseline),
            "verify": verify_baseline(repo, baseline),
        }
        result = results
    else:  # pragma: no cover
        raise AssertionError(command)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if command in {"verify", "verify-static-patch"}:
        return 0 if result.get("status") == "PASS" else 1
    if command == "run-all":
        verify_status = result.get("verify", {}).get("status")
        final_status = result.get("finalize", {}).get("status")
        return 0 if verify_status == "PASS" and final_status in {"ACCEPTED", "BLOCKED"} else 1
    return 0 if result.get("status") not in {"FAILED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
