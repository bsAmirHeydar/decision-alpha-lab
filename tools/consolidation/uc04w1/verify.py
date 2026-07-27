from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from tools.consolidation.ci.portable_hash import canonical_sha256
from tools.consolidation.uc04w0.verify import verify as verify_w0
from tools.consolidation.uc04w1.characterize import (
    CANDIDATE_ID,
    ENGINE_ID,
    FIXTURE_ROOT,
    HISTORICAL_CLUSTER_DIGEST,
    HISTORICAL_NORMALIZED_BODY_DIGEST,
    MEMBERS,
    PROPOSED_PRODUCTION_TARGET,
    REFERENCE_HEADER,
    REGISTRY_ROOT,
    SELF_TEST,
    canonical_digest,
    characterize,
    fixture_rows,
    load_historical_candidate,
    sha256_file,
)
from tools.repository_paths import RepositoryPaths

SCHEMA_ROOT = Path("schemas/consolidation/uc04/w1")
RELEASE_ROOT = Path("releases/unified_consolidation/uc04/w1")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
OUTPUT_RE = re.compile(r"^[0-9]{4}\.[0-9]{2}\.[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$")
REQUIRED_RECORDS = (
    "entry_decision.json",
    "candidate_inventory.json",
    "format_contract.json",
    "fixture_corpus.json",
    "reference_design.json",
    "static_equivalence_record.json",
    "consumer_cutover_plan.json",
    "native_acceptance_plan.json",
    "logic_preservation_certificate.json",
    "implementation_decision.json",
    "capability_migration_ledger.json",
    "w1a_exit_decision.json",
)
REQUIRED_SCHEMAS = (
    "entry_decision.schema.json",
    "candidate_inventory.schema.json",
    "datetime_format_contract.schema.json",
    "fixture_corpus.schema.json",
    "reference_design.schema.json",
    "static_equivalence_record.schema.json",
    "consumer_cutover_plan.schema.json",
    "native_acceptance_plan.schema.json",
    "logic_preservation_certificate.schema.json",
    "implementation_decision.schema.json",
    "capability_migration_ledger.schema.json",
    "w1a_exit_decision.schema.json",
)
AUTHORITY_FIELDS = (
    "semantic_change",
    "implementation_authority",
    "implementation_authorized",
    "production_materialization_authorized",
    "consumer_cutover_authority",
    "consumer_cutover_authorized",
    "deletion_authority",
    "runtime_authority",
    "order_authority",
    "capital_authority",
    "source_move_authorized",
    "source_delete_authorized",
)
REFERENCE_FORBIDDEN_TOKENS = (
    "OrderSend",
    "CTrade",
    "PositionOpen",
    "Buy(",
    "Sell(",
    "WebRequest",
    "FileOpen",
    "FileWrite",
    "ObjectCreate",
    "ObjectSet",
    "TimeCurrent",
    "TimeTradeServer",
    "TimeLocal",
    "CopyRates",
    "CopyBuffer",
    "iTime",
    "iClose",
    "SymbolInfoTick",
    "OnTick",
    "OnTimer",
)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root is not an object: {path}")
    return value


def verify_digest(relative: str, value: dict[str, Any], errors: list[str]) -> None:
    digest = value.get("document_digest")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        errors.append(f"missing or invalid document_digest: {relative}")
        return
    if digest != canonical_digest(value):
        errors.append(f"document_digest mismatch: {relative}")


def verify_no_authority(value: Any, label: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for field, item in value.items():
            if field in AUTHORITY_FIELDS and item is True:
                errors.append(f"W1A grants forbidden authority: {label}:{field}")
            verify_no_authority(item, f"{label}/{field}", errors)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            verify_no_authority(item, f"{label}/{index}", errors)


def verify_schema(instance_path: Path, schema_path: Path, errors: list[str]) -> None:
    try:
        instance = read_json(instance_path)
        schema = read_json(schema_path)
        Draft202012Validator.check_schema(schema)
        for issue in sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda item: list(item.path)):
            location = "/".join(str(part) for part in issue.path) or "<root>"
            errors.append(f"schema violation {instance_path.as_posix()} at {location}: {issue.message}")
    except Exception as exc:
        errors.append(f"schema validation failed {instance_path.as_posix()}: {exc}")


def verify_upstream_authority(repo: Path, errors: list[str]) -> None:
    w0_exit = read_json(repo / "registry/consolidation/uc04/w0/w0_exit_decision.json")
    candidate = read_json(repo / "registry/consolidation/uc04/w0/first_candidate_registration.json")
    if w0_exit.get("status") != "ACCEPTED" or w0_exit.get("next_wave") != "UC04-W1":
        errors.append("UC04-W0 does not provide an accepted handoff to UC04-W1")
    if candidate.get("status") != "AUTHORIZED_FOR_CHARACTERIZATION_ONLY":
        errors.append("UC04-W0 candidate is not characterization-only")
    for field in ("implementation_authority", "consumer_cutover_authority", "semantic_merge_authority", "deletion_authority"):
        if candidate.get(field) is not False:
            errors.append(f"UC04-W0 candidate handoff has unsafe {field}")


def verify_records(repo: Path, errors: list[str]) -> dict[str, dict[str, Any]]:
    actual: dict[str, dict[str, Any]] = {}
    for name in REQUIRED_SCHEMAS:
        schema_path = repo / SCHEMA_ROOT / name
        if not schema_path.is_file():
            errors.append(f"missing W1A schema: {name}")
            continue
        try:
            Draft202012Validator.check_schema(read_json(schema_path))
        except Exception as exc:
            errors.append(f"invalid W1A schema {name}: {exc}")

    expected_documents: dict[str, dict[str, Any]] = {}
    try:
        expected_documents = characterize(repo)
    except Exception as exc:
        errors.append(f"candidate characterization failed: {exc}")

    for name in REQUIRED_RECORDS:
        path = repo / REGISTRY_ROOT / name
        if not path.is_file():
            errors.append(f"missing W1A registry record: {name}")
            continue
        try:
            document = read_json(path)
        except Exception as exc:
            errors.append(f"invalid W1A registry record {name}: {exc}")
            continue
        actual[name] = document
        verify_digest(f"{REGISTRY_ROOT.as_posix()}/{name}", document, errors)
        verify_no_authority(document, name, errors)
        schema_name = Path(str(document.get("$schema", ""))).name
        if schema_name not in REQUIRED_SCHEMAS:
            errors.append(f"record references unknown schema: {name}: {schema_name}")
        elif (repo / SCHEMA_ROOT / schema_name).is_file():
            verify_schema(path, repo / SCHEMA_ROOT / schema_name, errors)
        expected = expected_documents.get(name)
        if expected is not None and document != expected:
            errors.append(f"stored characterization record is not reproducible: {name}")
    return actual


def verify_candidate(repo: Path, records: dict[str, dict[str, Any]], errors: list[str]) -> None:
    inventory = records.get("candidate_inventory.json", {})
    if inventory.get("candidate_id") != CANDIDATE_ID or inventory.get("engine_id") != ENGINE_ID:
        errors.append("candidate or engine identity drift")
    if inventory.get("historical_candidate_digest") != HISTORICAL_CLUSTER_DIGEST:
        errors.append("historical candidate digest drift")
    if inventory.get("historical_normalized_body_sha256") != HISTORICAL_NORMALIZED_BODY_DIGEST:
        errors.append("historical normalized body digest drift")
    if inventory.get("consumer_count") != 10 or inventory.get("active_call_site_count") != 41:
        errors.append("candidate topology must remain 10 consumers and 41 active call sites")
    if inventory.get("distinct_function_body_count") != 1:
        errors.append("candidate functions are not one exact body cluster")

    members = inventory.get("members", [])
    expected_pairs = {(path, name) for path, name, _ in MEMBERS}
    actual_pairs = {(str(row.get("artifact_path")), str(row.get("function_name"))) for row in members if isinstance(row, dict)}
    if actual_pairs != expected_pairs:
        errors.append("candidate member set drift")

    historical = load_historical_candidate(repo)
    historical_hashes = {str(row["artifact_path"]): str(row["artifact_sha256"]) for row in historical.get("members", [])}
    for path, _, _ in MEMBERS:
        target = repo / path
        if not target.is_file():
            errors.append(f"candidate source missing: {path}")
        elif sha256_file(target) != historical_hashes.get(path):
            errors.append(f"candidate source changed before native acceptance: {path}")


def verify_fixture_contract(repo: Path, records: dict[str, dict[str, Any]], errors: list[str]) -> None:
    corpus = records.get("fixture_corpus.json", {})
    rows = corpus.get("fixtures", [])
    if rows != fixture_rows():
        errors.append("registry fixture corpus drift")
    fixture_path = repo / FIXTURE_ROOT / "datetime_format_vectors.json"
    if not fixture_path.is_file():
        errors.append("missing standalone W1A fixture corpus")
        return
    standalone = read_json(fixture_path)
    if standalone.get("fixtures") != fixture_rows() or standalone.get("fixture_count") != 13:
        errors.append("standalone fixture corpus is not reproducible")
    outputs: list[str] = []
    seconds: list[int] = []
    for row in rows:
        expected = str(row.get("expected", ""))
        if len(expected.encode("ascii", errors="ignore")) != 19 or not OUTPUT_RE.fullmatch(expected):
            errors.append(f"fixture output violates byte-exact format: {row.get('fixture_id')}")
        try:
            expected.encode("ascii")
        except UnicodeEncodeError:
            errors.append(f"fixture output is not ASCII: {row.get('fixture_id')}")
        if expected[4:5] != "." or expected[7:8] != "." or expected[10:11] != " " or expected[13:14] != ":" or expected[16:17] != ":":
            errors.append(f"fixture punctuation offsets drift: {row.get('fixture_id')}")
        outputs.append(expected)
        seconds.append(int(row.get("unix_seconds", -1)))
    if seconds != sorted(seconds) or outputs != sorted(outputs):
        errors.append("fixture corpus does not preserve chronological/lexicographic order")


def verify_reference_boundary(repo: Path, records: dict[str, dict[str, Any]], errors: list[str]) -> None:
    design = records.get("reference_design.json", {})
    reference = repo / REFERENCE_HEADER
    self_test = repo / SELF_TEST
    if not reference.is_file() or not self_test.is_file():
        errors.append("W1A test-only reference or native self-test is missing")
        return
    if design.get("reference_header_sha256") != sha256_file(reference):
        errors.append("reference header hash drift")
    if design.get("native_self_test_sha256") != sha256_file(self_test):
        errors.append("native self-test hash drift")
    if not REFERENCE_HEADER.as_posix().startswith("mql5/Tests/") or not SELF_TEST.as_posix().startswith("mql5/Tests/"):
        errors.append("W1A reference artifacts escaped the test-only boundary")
    if (repo / PROPOSED_PRODUCTION_TARGET).exists():
        errors.append("production shared engine was materialized without authority")

    reference_text = reference.read_text(encoding="utf-8-sig")
    for token in REFERENCE_FORBIDDEN_TOKENS:
        if token in reference_text:
            errors.append(f"test-only reference contains forbidden capability token: {token}")
    required = (
        "MqlDateTime dt;",
        "TimeToStruct(value, dt);",
        'StringFormat("%04d.%02d.%02d %02d:%02d:%02d"',
    )
    for token in required:
        if token not in reference_text:
            errors.append(f"test-only reference missing deterministic legacy token: {token}")
    self_test_text = self_test.read_text(encoding="utf-8-sig")
    for token in ("#property strict", "FILE_COMMON", "UC04-W1A SELFTEST PASS", "ArraySize(values)"):
        if token not in self_test_text:
            errors.append(f"native self-test missing acceptance token: {token}")
    if any(token in self_test_text for token in ("OrderSend", "CTrade", "PositionOpen", "WebRequest", "ObjectCreate")):
        errors.append("native self-test acquired a forbidden execution/network/chart capability")


def verify_pending_native_status(records: dict[str, dict[str, Any]], errors: list[str]) -> None:
    static = records.get("static_equivalence_record.json", {})
    plan = records.get("native_acceptance_plan.json", {})
    certificate = records.get("logic_preservation_certificate.json", {})
    decision = records.get("implementation_decision.json", {})
    exit_decision = records.get("w1a_exit_decision.json", {})
    expected = (
        (static.get("native_compile_result"), "PENDING_LOCAL_WINDOWS"),
        (static.get("native_runtime_result"), "PENDING_LOCAL_WINDOWS"),
        (plan.get("native_compile_performed"), False),
        (plan.get("native_runtime_performed"), False),
        (certificate.get("status"), "BLOCKED_PENDING_NATIVE_EVIDENCE"),
        (decision.get("production_materialization_authorized"), False),
        (decision.get("consumer_cutover_authorized"), False),
        (exit_decision.get("status"), "CHARACTERIZATION_ACCEPTED_IMPLEMENTATION_BLOCKED"),
        (exit_decision.get("next_delivery"), "UC04-W1B_NATIVE_QUALIFICATION_AND_BOUNDED_CUTOVER"),
    )
    for actual, wanted in expected:
        if actual != wanted:
            errors.append(f"native/authority state drift: {actual!r} != {wanted!r}")


def verify_release(repo: Path, errors: list[str]) -> None:
    release = repo / RELEASE_ROOT
    required = {
        "README.md", "INSTALL.md", "ROLLBACK.md", "COMMIT_MESSAGE.txt", "APPLY.ps1",
        "PATCH_MANIFEST.json", "PATCH_FILE_INDEX.txt", "PATCH_FILE_HASHES.sha256", "QA_REPORT.json",
    }
    if not release.is_dir():
        errors.append(f"release directory missing: {RELEASE_ROOT.as_posix()}")
        return
    present = {path.name for path in release.iterdir() if path.is_file()}
    if required - present:
        errors.append(f"release controls missing: {sorted(required - present)}")
        return
    index = [line.strip().replace("\\", "/") for line in (release / "PATCH_FILE_INDEX.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
    if index != sorted(set(index)):
        errors.append("W1A patch index is not sorted and unique")
    for relative in index:
        if not (repo / relative).is_file():
            errors.append(f"W1A patch index target missing: {relative}")
    ledger: dict[str, str] = {}
    for line in (release / "PATCH_FILE_HASHES.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            digest, relative = line.split("  ", 1)
        except ValueError:
            errors.append(f"invalid W1A hash-ledger line: {line}")
            continue
        ledger[relative.replace("\\", "/")] = "sha256:" + digest.removeprefix("sha256:")
    expected_hashed = set(index) - {f"{RELEASE_ROOT.as_posix()}/PATCH_FILE_HASHES.sha256"}
    if set(ledger) != expected_hashed:
        errors.append("W1A patch hash-ledger paths do not match patch index")
    for relative, expected in ledger.items():
        target = repo / relative
        if target.is_file() and "sha256:" + canonical_sha256(target) != expected:
            errors.append(f"W1A patch hash mismatch: {relative}")
    manifest = read_json(release / "PATCH_MANIFEST.json")
    if manifest.get("patch_file_count") != len(index) or manifest.get("hash_ledger_entry_count") != len(ledger):
        errors.append("W1A patch manifest count mismatch")
    if manifest.get("status") != "CHARACTERIZATION_ACCEPTED_IMPLEMENTATION_BLOCKED":
        errors.append("W1A release manifest misstates acceptance boundary")
    verify_no_authority(manifest, "release_manifest", errors)
    qa = read_json(release / "QA_REPORT.json")
    if qa.get("native_metaeditor") != "PENDING_LOCAL_WINDOWS" or qa.get("native_runtime") != "PENDING_LOCAL_WINDOWS":
        errors.append("W1A QA report falsely claims native acceptance")


def verify(repo: Path, *, verify_release_controls: bool = True, verify_upstream_w0: bool = True) -> list[str]:
    root = RepositoryPaths.discover(repo).root
    errors: list[str] = []
    if verify_upstream_w0:
        errors.extend(f"upstream W0: {error}" for error in verify_w0(root, verify_release_controls=False))
    verify_upstream_authority(root, errors)
    records = verify_records(root, errors)
    verify_candidate(root, records, errors)
    verify_fixture_contract(root, records, errors)
    verify_reference_boundary(root, records, errors)
    verify_pending_native_status(records, errors)
    if verify_release_controls:
        verify_release(root, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify UC04-W1A deterministic MQL5 datetime formatter characterization.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--skip-release-controls", action="store_true")
    parser.add_argument("--skip-upstream-w0", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors = verify(
        Path(args.repo_root),
        verify_release_controls=not args.skip_release_controls,
        verify_upstream_w0=not args.skip_upstream_w0,
    )
    if args.json:
        print(json.dumps({"stage_id": "UC04-W1A", "status": "PASS" if not errors else "FAIL", "error_count": len(errors), "errors": errors}, indent=2))
    else:
        print(f"UC04-W1A errors: {len(errors)}")
        for error in errors[:200]:
            print("ERROR:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
