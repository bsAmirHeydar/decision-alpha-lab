from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from tools.consolidation.uc04w1.characterize import PROPOSED_PRODUCTION_TARGET, characterize
from tools.consolidation.uc04w1.verify import verify_complete_transition
from tools.consolidation.uc04w1b.contracts import BASELINE_COMPILE_TARGETS
from tools.consolidation.uc04w1bn1.contracts import (
    AUTHORITY_FIELDS,
    DOC_ROOT,
    EVIDENCE_EXPORTER,
    REGISTRY_ROOT,
    RELEASE_ROOT,
    RUNNER,
    SCHEMA_ROOT,
    canonical_digest,
    read_json,
    sha256_file,
)
from tools.consolidation.uc04w1bn1.records import build_records
from tools.repository_paths import RepositoryPaths

REQUIRED_RECORDS = (
    "entry_decision.json",
    "host_execution_contract.json",
    "evidence_export_policy.json",
    "exit_decision.json",
)
REQUIRED_SCHEMAS = (
    "entry_decision.schema.json",
    "host_execution_contract.schema.json",
    "evidence_export_policy.schema.json",
    "exit_decision.schema.json",
    "evidence_bundle_manifest.schema.json",
    "patch_manifest.schema.json",
    "qa_report.schema.json",
)
REQUIRED_DOCS = (
    "00_MOC.md",
    "01_Native_Host_Qualification_Hardening.md",
    "02_One_Click_Windows_Runbook.md",
    "03_Evidence_Bundle_And_Authority_Boundary.md",
)
REQUIRED_RELEASE = (
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


def _validate_schema(instance: dict[str, Any], schema: dict[str, Any], label: str, errors: list[str]) -> None:
    try:
        Draft202012Validator.check_schema(schema)
        for issue in sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda item: list(item.path)):
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
    w1b_exit = read_json(repo / "registry/consolidation/uc04/w1b/w1b_q_exit_decision.json")
    if w1b_exit.get("status") != "ACCEPTED_TOOLING_NATIVE_EXECUTION_PENDING":
        errors.append("W1B-Q is not in native-execution-pending status")
    if w1b_exit.get("native_execution_performed") is not False:
        errors.append("W1B-Q unexpectedly claims native execution")
    if (repo / PROPOSED_PRODUCTION_TARGET).exists():
        errors.append("production formatter materialized before native evidence")
    transition_errors: list[str] = []
    transition = verify_complete_transition(repo, transition_errors)
    if transition is None:
        try:
            characterize(repo)
        except Exception as exc:
            errors.append(f"W1A characterization replay failed: {exc}")
    else:
        errors.extend(f"W1A transition: {item}" for item in transition_errors)


def _verify_records(repo: Path, errors: list[str]) -> None:
    expected = build_records(repo)
    for name in REQUIRED_SCHEMAS:
        path = repo / SCHEMA_ROOT / name
        if not path.is_file():
            errors.append(f"missing W1B-N1 schema: {name}")
            continue
        try:
            Draft202012Validator.check_schema(read_json(path))
        except Exception as exc:
            errors.append(f"invalid W1B-N1 schema {name}: {exc}")

    for name in REQUIRED_RECORDS:
        path = repo / REGISTRY_ROOT / name
        if not path.is_file():
            errors.append(f"missing W1B-N1 record: {name}")
            continue
        try:
            document = read_json(path)
        except Exception as exc:
            errors.append(f"invalid W1B-N1 record {name}: {exc}")
            continue
        if document.get("document_digest") != canonical_digest(document):
            errors.append(f"document digest mismatch: {name}")
        _verify_no_authority(document, name, errors)
        schema_name = Path(str(document.get("$schema", ""))).name
        schema_path = repo / SCHEMA_ROOT / schema_name
        if not schema_path.is_file():
            errors.append(f"unknown schema reference: {name}:{schema_name}")
        else:
            _validate_schema(document, read_json(schema_path), name, errors)
        if document != expected.get(name):
            errors.append(f"stored W1B-N1 record is not reproducible: {name}")


def _verify_runner(repo: Path, errors: list[str]) -> None:
    path = repo / RUNNER
    if not path.is_file():
        errors.append("W1B-N1 Windows runner missing")
        return
    payload = path.read_bytes()
    if not payload.endswith(b"\r\n") or payload.count(b"\n") != payload.count(b"\r\n"):
        errors.append("W1B-N1 Windows runner must use CRLF")
    text = payload.decode("utf-8-sig")
    required = (
        '"/compile:$Source"',
        '"/include:$WorkspaceMql5"',
        '"/log"',
        "0\\s+errors?\\s*,\\s*0\\s+warnings?",
        "PYTHONDONTWRITEBYTECODE",
        'Prefix = @("-B")',
        'Prefix = @("-3", "-B")',
        "Get-TrackedState",
        "--untracked-files=no",
        "AllowLiveTrading=0",
        "AllowDllImport=0",
        "ShutdownTerminal=1",
        "Assert-TerminalNotRunning",
        "LOCALAPPDATA",
        "ProgramData",
        "APPDATA",
        "tools.consolidation.uc04w1b.native_review",
        "tools.consolidation.uc04w1b.cutover_candidate",
        "tools.consolidation.uc04w1bn1.evidence_export",
        "Production cutover was not applied. Git was not modified.",
    )
    for token in required:
        if token not in text:
            errors.append(f"W1B-N1 runner missing control: {token}")
    for forbidden in ("git add", "git commit", "git push", "OrderSend(", "CTrade"):
        if forbidden.lower() in text.lower():
            errors.append(f"W1B-N1 runner contains forbidden capability: {forbidden}")
    for target in BASELINE_COMPILE_TARGETS:
        if f'"{target}"' not in text:
            errors.append(f"W1B-N1 compile target missing: {target}")
    if text.count('"mql5/') < len(BASELINE_COMPILE_TARGETS):
        errors.append("W1B-N1 compile matrix is incomplete")


def _verify_exporter(repo: Path, errors: list[str]) -> None:
    path = repo / EVIDENCE_EXPORTER
    if not path.is_file():
        errors.append("W1B-N1 evidence exporter missing")
        return
    text = path.read_text(encoding="utf-8-sig")
    for token in (
        "host_paths_redacted",
        "secret_material_included",
        "account_identifiers_included",
        "native_acceptance_receipt.sanitized.json",
        "bundle_manifest.json",
        "apply_authorized",
    ):
        if token not in text:
            errors.append(f"W1B-N1 evidence exporter missing control: {token}")
    for forbidden in ("password", "broker_credentials", "private_key"):
        if f'[{forbidden!r}]' in text:
            errors.append(f"W1B-N1 evidence exporter contains suspicious secret field: {forbidden}")


def _verify_docs_release(repo: Path, errors: list[str]) -> None:
    for name in REQUIRED_DOCS:
        if not (repo / DOC_ROOT / name).is_file():
            errors.append(f"missing W1B-N1 document: {name}")
    release = repo / RELEASE_ROOT
    for name in REQUIRED_RELEASE:
        if not (release / name).is_file():
            errors.append(f"missing W1B-N1 release control: {name}")
    index_path = release / "PATCH_FILE_INDEX.txt"
    ledger_path = release / "PATCH_FILE_HASHES.sha256"
    if index_path.is_file() and ledger_path.is_file():
        index = [
            line.strip().replace("\\", "/")
            for line in index_path.read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        ]
        if index != sorted(set(index)):
            errors.append("W1B-N1 patch index is not sorted and unique")
        for relative in index:
            if not (repo / relative).is_file():
                errors.append(f"W1B-N1 indexed file missing: {relative}")
        ledger: dict[str, str] = {}
        for line in ledger_path.read_text(encoding="utf-8-sig").splitlines():
            if not line.strip():
                continue
            try:
                digest, relative = line.split("  ", 1)
            except ValueError:
                errors.append(f"invalid W1B-N1 hash row: {line}")
                continue
            ledger[relative.replace("\\", "/")] = digest.lower()
        expected = set(index) - {"releases/unified_consolidation/uc04/w1bn1/PATCH_FILE_HASHES.sha256"}
        if set(ledger) != expected:
            errors.append("W1B-N1 hash ledger paths do not match patch index")
        transition_active = (repo / "registry/consolidation/uc04/complete/w1_candidate_transition.json").is_file()
        immutable_prefixes = (
            "releases/unified_consolidation/uc04/w1bn1/",
            "registry/consolidation/uc04/w1bn1/",
            "schemas/consolidation/uc04/w1bn1/",
            "docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/18_UC04_W1B_NATIVE_HOST_HARDENING/",
        )
        for relative, digest in ledger.items():
            path = repo / relative
            must_match = (not transition_active) or relative.startswith(immutable_prefixes)
            if must_match and path.is_file() and sha256_file(path).removeprefix("sha256:") != digest:
                errors.append(f"W1B-N1 patch hash mismatch: {relative}")

        manifest_path = release / "PATCH_MANIFEST.json"
        qa_path = release / "QA_REPORT.json"
        if manifest_path.is_file():
            manifest = read_json(manifest_path)
            _validate_schema(manifest, read_json(repo / SCHEMA_ROOT / "patch_manifest.schema.json"), "PATCH_MANIFEST.json", errors)
            if manifest.get("patch_file_count") != len(index):
                errors.append("W1B-N1 manifest patch_file_count mismatch")
            if manifest.get("hash_ledger_entry_count") != len(expected):
                errors.append("W1B-N1 manifest hash_ledger_entry_count mismatch")
            if manifest.get("added_file_count") != len(index):
                errors.append("W1B-N1 manifest added_file_count mismatch")
        if qa_path.is_file():
            qa = read_json(qa_path)
            _validate_schema(qa, read_json(repo / SCHEMA_ROOT / "qa_report.schema.json"), "QA_REPORT.json", errors)

    apply = release / "APPLY.ps1"
    if apply.is_file():
        text = apply.read_text(encoding="utf-8-sig").lower()
        for forbidden in ("git add .", "git add -a", "git commit", "git push"):
            if forbidden in text:
                errors.append(f"W1B-N1 installer contains forbidden Git action: {forbidden}")
        for token in ("run_engineering_policy.py", "uc04w0.verify", "uc04w1.verify", "uc04w1b.verify", "uc04w1bn1.verify", "pytest", "--collect-only"):
            if token not in text:
                errors.append(f"W1B-N1 installer missing validation: {token}")


def verify(repo: Path) -> list[str]:
    root = RepositoryPaths.discover(repo).root
    errors: list[str] = []
    _verify_upstream(root, errors)
    _verify_records(root, errors)
    _verify_runner(root, errors)
    _verify_exporter(root, errors)
    _verify_docs_release(root, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify UC04-W1B-N1 native host hardening.")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    errors = verify(Path(args.repo_root))
    if errors:
        print(f"UC04-W1B-N1 errors: {len(errors)}")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("UC04-W1B-N1 verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
