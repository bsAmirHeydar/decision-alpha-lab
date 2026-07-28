from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from tools.repository_paths import RepositoryPaths
from tools.consolidation.uc04w1.characterize import PROPOSED_PRODUCTION_TARGET, characterize
from tools.consolidation.uc04w1.verify import verify_complete_transition
from tools.consolidation.uc04w1b.contracts import (
    AUTHORITY_FIELDS,
    BASELINE_COMPILE_TARGETS,
    DOC_ROOT,
    NATIVE_RUNNER_SOURCE,
    REGISTRY_ROOT,
    RELEASE_ROOT,
    SCHEMA_ROOT,
    canonical_digest,
    read_json,
    sha256_file,
)
from tools.consolidation.uc04w1b.records import build_records
from tools.consolidation.uc04w1b.package_validation import PackageValidationError, verify_tree

REQUIRED_RECORDS = (
    "entry_decision.json",
    "native_execution_contract.json",
    "evidence_review_policy.json",
    "conditional_cutover_policy.json",
    "w1b_q_exit_decision.json",
)
REQUIRED_SCHEMAS = (
    "entry_decision.schema.json",
    "native_execution_contract.schema.json",
    "evidence_review_policy.schema.json",
    "conditional_cutover_policy.schema.json",
    "w1b_q_exit_decision.schema.json",
    "independent_native_review.schema.json",
    "cutover_candidate_manifest.schema.json",
    "rollback_manifest.schema.json",
    "patch_manifest.schema.json",
    "qa_report.schema.json",
)
REQUIRED_DOCS = (
    "00_MOC.md",
    "01_Native_Qualification_Execution_Contract.md",
    "02_Evidence_Review_And_Conditional_Cutover.md",
    "03_Windows_Runbook.md",
    "04_Authority_And_Safety_Boundary.md",
    "05_Installable_Release_And_Rollback.md",
)
FORBIDDEN_MQL5_TOKENS = (
    "OrderSend(",
    "CTrade",
    "PositionOpen(",
    "Buy(",
    "Sell(",
    "WebRequest(",
    "SocketCreate(",
    "TimeCurrent(",
    "TimeTradeServer(",
    "SymbolInfoTick(",
    "CopyRates(",
    "iTime(",
    "iClose(",
)


def _verify_schema(instance: dict[str, Any], schema: dict[str, Any], label: str, errors: list[str]) -> None:
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for issue in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
            location = "/".join(str(part) for part in issue.path) or "<root>"
            errors.append(f"schema violation {label} at {location}: {issue.message}")
    except Exception as exc:
        errors.append(f"schema validation failed {label}: {exc}")


def _verify_no_authority(value: Any, label: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in AUTHORITY_FIELDS and item is True:
                errors.append(f"forbidden authority in {label}: {key}")
            _verify_no_authority(item, f"{label}/{key}", errors)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _verify_no_authority(item, f"{label}/{index}", errors)


def _verify_upstream(repo: Path, errors: list[str]) -> None:
    qa = read_json(repo / "releases/unified_consolidation/uc04/w1/QA_REPORT.json")
    exit_decision = read_json(repo / "registry/consolidation/uc04/w1/w1a_exit_decision.json")
    implementation = read_json(repo / "registry/consolidation/uc04/w1/implementation_decision.json")
    if qa.get("status") != "PASS_CHARACTERIZATION_IMPLEMENTATION_BLOCKED":
        errors.append("UC04-W1A QA status does not authorize native qualification tooling")
    if exit_decision.get("status") != "CHARACTERIZATION_ACCEPTED_IMPLEMENTATION_BLOCKED":
        errors.append("UC04-W1A exit decision drift")
    if implementation.get("status") != "BLOCKED_PENDING_NATIVE_EVIDENCE":
        errors.append("UC04-W1A implementation decision drift")
    if (repo / PROPOSED_PRODUCTION_TARGET).exists():
        errors.append("production shared engine materialized before native acceptance")
    transition_errors: list[str] = []
    transition = verify_complete_transition(repo, transition_errors)
    if transition is None:
        try:
            characterize(repo)
        except Exception as exc:
            errors.append(f"W1A candidate replay failed: {exc}")
    else:
        errors.extend(f"W1A transition: {item}" for item in transition_errors)


def _verify_records(repo: Path, errors: list[str]) -> None:
    expected = build_records(repo)
    for name in REQUIRED_SCHEMAS:
        path = repo / SCHEMA_ROOT / name
        if not path.is_file():
            errors.append(f"missing W1B schema: {name}")
            continue
        try:
            Draft202012Validator.check_schema(read_json(path))
        except Exception as exc:
            errors.append(f"invalid W1B schema {name}: {exc}")

    for name in REQUIRED_RECORDS:
        path = repo / REGISTRY_ROOT / name
        if not path.is_file():
            errors.append(f"missing W1B registry record: {name}")
            continue
        try:
            document = read_json(path)
        except Exception as exc:
            errors.append(f"invalid W1B registry record {name}: {exc}")
            continue
        if document.get("document_digest") != canonical_digest(document):
            errors.append(f"document digest mismatch: {name}")
        _verify_no_authority(document, name, errors)
        schema_name = Path(str(document.get("$schema", ""))).name
        schema_path = repo / SCHEMA_ROOT / schema_name
        if not schema_path.is_file():
            errors.append(f"unknown schema reference: {name}:{schema_name}")
        else:
            _verify_schema(document, read_json(schema_path), name, errors)
        if document != expected.get(name):
            errors.append(f"stored W1B record is not reproducible: {name}")


def _verify_native_runner(repo: Path, errors: list[str]) -> None:
    path = repo / NATIVE_RUNNER_SOURCE
    if not path.is_file():
        errors.append("native MQL5 runner missing")
        return
    text = path.read_text(encoding="utf-8-sig")
    if "void OnStart()" not in text or "FILE_COMMON" not in text:
        errors.append("native MQL5 runner is not a FILE_COMMON script")
    if text.count("D'") != 13 or text.count('"1970.01.01 00:00:00"') != 1:
        errors.append("native MQL5 runner fixture corpus drift")
    for token in FORBIDDEN_MQL5_TOKENS:
        if token in text:
            errors.append(f"native MQL5 runner contains forbidden capability: {token}")
    if "AL_UC04W1_ReferenceFormatDateTime" not in text:
        errors.append("native MQL5 runner does not execute the frozen reference")
    if "UC04W1B_DeterministicDateTimeFormatNativeRunner.csv" not in text:
        errors.append("native MQL5 runner output identity drift")


def _verify_powershell(repo: Path, errors: list[str]) -> None:
    path = repo / "tools/consolidation/uc04w1b/Invoke-UC04W1BQualification.ps1"
    if not path.is_file():
        errors.append("Windows native qualification orchestrator missing")
        return
    text = path.read_text(encoding="utf-8-sig")
    required = (
        'AllowLiveTrading=0',
        'AllowDllImport=0',
        'ShutdownTerminal=1',
        'Assert-TerminalNotRunning',
        'finally {',
        'tracked_source_mutation = $false',
        'consumer_cutover_authority = $false',
        'tools.consolidation.uc04w1b.native_review',
        'tools.consolidation.uc04w1b.cutover_candidate',
    )
    for token in required:
        if token not in text:
            errors.append(f"native qualification orchestrator missing safety control: {token}")
    for forbidden in ("git add", "git commit", "git push", "Remove-Item -Recurse $Root"):
        if forbidden.lower() in text.lower():
            errors.append(f"native qualification orchestrator contains forbidden repository action: {forbidden}")
    for target in BASELINE_COMPILE_TARGETS:
        if f'"{target}"' not in text:
            errors.append(f"native qualification compile target missing: {target}")


def _verify_docs(repo: Path, errors: list[str]) -> None:
    for name in REQUIRED_DOCS:
        path = repo / DOC_ROOT / name
        if not path.is_file():
            errors.append(f"missing W1B canonical document: {name}")


def _verify_release(repo: Path, errors: list[str]) -> None:
    release = repo / RELEASE_ROOT
    required = (
        "README.md",
        "INSTALL.md",
        "ROLLBACK.md",
        "COMMIT_MESSAGE.txt",
        "PATCH_FILE_INDEX.txt",
        "PATCH_FILE_HASHES.sha256",
        "PATCH_MANIFEST.json",
        "QA_REPORT.json",
        "APPLY.ps1",
    )
    for name in required:
        if not (release / name).is_file():
            errors.append(f"missing W1B release file: {name}")

    apply_path = release / "APPLY.ps1"
    install_path = release / "INSTALL.md"
    if apply_path.is_file():
        apply_text = apply_path.read_text(encoding="utf-8-sig")
        for token in (
            'ValidateSet("Install", "Rollback")',
            "Assert-TargetPathsClean",
            "Copy-Atomic",
            "Restore-InstallationState",
            "verify-tree",
            "pytest_collection",
        ):
            if token not in apply_text:
                errors.append(f"W1B installer missing safety control: {token}")
        for forbidden in ("git add .", "git add -A", "git commit", "git push"):
            if forbidden.lower() in apply_text.lower():
                errors.append(f"W1B installer contains forbidden Git action: {forbidden}")
    if install_path.is_file():
        install_text = install_path.read_text(encoding="utf-8-sig")
        for token in (
            "Expand-Archive -LiteralPath",
            "Get-FileHash -LiteralPath",
            "PATCH_FILE_INDEX.txt",
            "PATCH_FILE_HASHES.sha256",
            "git add --pathspec-from-file",
        ):
            if token not in install_text:
                errors.append(f"W1B INSTALL.md missing required command/control: {token}")
        if "git push" in install_text.lower():
            errors.append("W1B INSTALL.md must not instruct push")

    transition_errors: list[str] = []
    transition = verify_complete_transition(repo, transition_errors)
    if transition is None:
        try:
            verify_tree(repo)
        except PackageValidationError as exc:
            errors.append(f"W1B installable package contract failed: {exc}")
    else:
        errors.extend(f"W1B transition: {item}" for item in transition_errors)


def verify(repo: Path) -> list[str]:
    root = RepositoryPaths.discover(repo).root
    errors: list[str] = []
    _verify_upstream(root, errors)
    _verify_records(root, errors)
    _verify_native_runner(root, errors)
    _verify_powershell(root, errors)
    _verify_docs(root, errors)
    _verify_release(root, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify UC04-W1B native qualification tooling.")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    errors = verify(Path(args.repo_root))
    if errors:
        print("UC04-W1B verification: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("UC04-W1B verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
