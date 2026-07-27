from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from tools.consolidation.ci.portable_hash import canonical_sha256
from tools.repository_paths import RepositoryPaths, migrated_relative_path

REGISTRY_ROOT = Path("registry/consolidation/uc04/w0")
SCHEMA_ROOT = Path("schemas/consolidation/uc04")
RELEASE_ROOT = Path("releases/unified_consolidation/uc04/w0")
SHA256_RE = re.compile(r"^(?:sha256:)?[0-9a-f]{64}$")
AUTHORITY_FIELDS = (
    "semantic_change",
    "semantic_merge_authority",
    "deletion_authority",
    "runtime_authority",
    "order_authority",
    "capital_authority",
    "runtime_authority_created",
    "order_authority_created",
    "capital_authority_created",
)
REQUIRED_REGISTRY = (
    "entry_decision.json",
    "scope_manifest.json",
    "path_contract.json",
    "test_recovery_receipt.json",
    "rthp_recovery_receipt.json",
    "semantic_baseline_freeze.json",
    "capability_migration_ledger.json",
    "first_candidate_registration.json",
    "uc01_static_amendment.json",
    "uc03_post_closure_amendment.json",
    "obsidian_foundation_amendment.json",
    "w0_exit_decision.json",
)
REQUIRED_SCHEMAS = (
    "path_contract.schema.json",
    "capability_migration_ledger_row.schema.json",
    "logic_preservation_certificate.schema.json",
    "semantic_equivalence_record.schema.json",
    "consumer_cutover_record.schema.json",
    "quarantine_record.schema.json",
    "w0_exit_decision.schema.json",
)
RTHP_REGISTRATIONS = (
    "registry/history/strategy_factory/contexts/rthp/v1/context_package_registration.json",
    "registry/history/strategy_factory/contexts/rthp/v1/rthp_ai_input_registration.json",
    "registry/history/strategy_factory/contexts/rthp/v1/acl03_onboarding_registration.json",
)
FORBIDDEN_ACTIVE_PREFIXES = (
    "lab/11_strategy_factory",
    "registry/strategy_factory",
    "registry/acl_os",
    "docs/alpha_lab_master_architecture",
)
ACTIVE_RTHP_ROOTS = (
    "src/engine/packages/strategy_factory_rthp_train_activation_v1",
    "src/engine/packages/strategy_factory_rthp_mt5_activation_v1",
    "src/engine/tooling/strategy_factory/acl_os",
)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root is not an object: {path}")
    return value


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_logical_text_file(path: Path) -> str:
    """Hash text artifacts using the repository's LF logical representation.

    UC04 relocation amendments cover text artifacts.  Git may materialize those
    artifacts with CRLF in a Windows worktree even though their committed form
    and recorded amendment digest use LF.  Normalizing only this evidence path
    preserves byte-exact checks for baselines and release ledgers.
    """
    content = path.read_bytes().replace(b"\r\n", b"\n")
    if path.suffix.lower() in {".bat", ".cmd", ".ps1"}:
        content = content.replace(b"\n", b"\r\n")
    return "sha256:" + hashlib.sha256(content).hexdigest()


def canonical_digest(value: dict[str, Any], omitted_field: str) -> str:
    material = {key: item for key, item in value.items() if key != omitted_field}
    payload = json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def verify_document_digest(path: Path, value: dict[str, Any], errors: list[str]) -> None:
    field = "amendment_digest" if "amendment_digest" in value else "document_digest"
    actual = value.get(field)
    if not isinstance(actual, str) or not SHA256_RE.fullmatch(actual):
        errors.append(f"missing or invalid {field}: {path.as_posix()}")
        return
    if actual != canonical_digest(value, field):
        errors.append(f"{field} mismatch: {path.as_posix()}")


def verify_no_authority(value: dict[str, Any], label: str, errors: list[str]) -> None:
    for field in AUTHORITY_FIELDS:
        if value.get(field) is True:
            errors.append(f"UC04-W0 grants forbidden authority: {label}: {field}")


def validate_schema(instance_path: Path, schema_path: Path, errors: list[str]) -> None:
    try:
        instance = read_json(instance_path)
        schema = read_json(schema_path)
        validator = Draft202012Validator(schema)
        for issue in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
            location = "/".join(str(item) for item in issue.path) or "<root>"
            errors.append(f"schema violation {instance_path.as_posix()} at {location}: {issue.message}")
    except Exception as exc:
        errors.append(f"schema validation failed for {instance_path.as_posix()}: {exc}")


def verify_path_contract(repo: Path, document: dict[str, Any], errors: list[str]) -> None:
    paths = RepositoryPaths.from_root(repo)
    expected_roots = {
        "source": paths.source_root,
        "packages": paths.package_root,
        "tooling": paths.tooling_root,
        "contexts": paths.context_root,
        "authored_strategy_factory_contexts": paths.authored_strategy_factory_context_root,
        "generated_strategy_factory_contexts": paths.generated_strategy_factory_context_root,
        "registry": paths.registry_root,
        "historical_registry": paths.historical_registry_root,
        "schemas": paths.schema_root,
        "documentation": paths.documentation_root,
        "releases": paths.release_root,
        "runtime_runs": paths.runtime_run_root,
    }
    actual_roots = document.get("canonical_roots", {})
    for key, target in expected_roots.items():
        expected = target.relative_to(repo).as_posix()
        if actual_roots.get(key) != expected:
            errors.append(f"path contract root mismatch: {key}: {actual_roots.get(key)!r} != {expected!r}")

    examples = {
        "lab/11_strategy_factory/python/strategy_factory_rthp_train_activation_v1/pipeline.py":
            "src/engine/packages/strategy_factory_rthp_train_activation_v1/pipeline.py",
        "tools/strategy_factory/acl_os/common.py":
            "src/engine/tooling/strategy_factory/acl_os/common.py",
        "registry/strategy_factory/contexts/rthp/v1/context_package_registration.json":
            "registry/history/strategy_factory/contexts/rthp/v1/context_package_registration.json",
        "registry/acl_os/acl_03/contexts/rthp/v1/semantic_approval.json":
            "registry/history/acl/acl_03/contexts/rthp/v1/semantic_approval.json",
        "docs/alpha_lab_master_architecture/context_lifecycle_os":
            "docs/architecture/master/context_lifecycle_os",
    }
    for legacy, expected in examples.items():
        actual = migrated_relative_path(repo, legacy)
        if actual != expected:
            errors.append(f"migration-aware path mismatch: {legacy} -> {actual}; expected {expected}")


def verify_pytest_contract(repo: Path, receipt: dict[str, Any], errors: list[str]) -> None:
    path = repo / "pytest.ini"
    if not path.is_file():
        errors.append("missing root pytest.ini")
        return
    text = path.read_text(encoding="utf-8")
    for token in ("--import-mode=importlib", "testpaths = tests", "src/engine/packages"):
        if token not in text:
            errors.append(f"pytest.ini missing canonical token: {token}")
    if receipt.get("collection_error_count") != 0:
        errors.append("test recovery receipt does not assert zero collection errors")
    if int(receipt.get("collected_test_count", 0)) < 9000:
        errors.append("test recovery receipt collected-test count is unexpectedly low")
    attempt = receipt.get("full_repository_suite_attempt", {})
    if attempt.get("status") != "INCOMPLETE_AT_FIRST_HISTORICAL_LFS_BLOCKER":
        errors.append("full repository suite limitation is missing or misclassified")
    if attempt.get("unresolved_beyond_first_blocker") is not True:
        errors.append("full repository suite must preserve unresolved-beyond-blocker status")
    pointers = attempt.get("git_lfs_pointer_paths", [])
    if len(pointers) != 4:
        errors.append("historical Git LFS pointer inventory must contain four paths")
    for relative in pointers:
        target = repo / str(relative)
        if not target.is_file() or not target.read_text(encoding="utf-8").startswith("version https://git-lfs.github.com/spec/v1"):
            errors.append(f"declared historical Git LFS pointer is missing or not a pointer: {relative}")


def verify_amendment(path: Path, value: dict[str, Any], errors: list[str]) -> None:
    if value.get("status") != "PASS" or value.get("stage_id") != "UC04-W0":
        errors.append(f"amendment is not an accepted UC04-W0 PASS document: {path.as_posix()}")
    rows = value.get("records", [])
    if not isinstance(rows, list) or value.get("record_count") != len(rows):
        errors.append(f"amendment record count mismatch: {path.as_posix()}")
        return
    for row in rows:
        if not isinstance(row, dict):
            errors.append(f"non-object amendment row: {path.as_posix()}")
            continue
        verify_no_authority(row, path.as_posix(), errors)
        for field in ("current_sha256", "previous_sha256"):
            digest = row.get(field)
            if digest is not None and (not isinstance(digest, str) or not SHA256_RE.fullmatch(digest)):
                errors.append(f"invalid amendment digest {field}: {path.as_posix()}")
        current_path = row.get("path") or row.get("current_path")
        current_digest = row.get("current_sha256")
        if isinstance(current_path, str) and isinstance(current_digest, str):
            target = path.parents[4] / current_path
            if not target.is_file():
                errors.append(f"amendment target missing: {current_path}")
            elif sha256_logical_text_file(target) != current_digest:
                errors.append(f"amendment current hash mismatch: {current_path}")


def verify_frozen_baseline(repo: Path, value: dict[str, Any], errors: list[str]) -> None:
    rows = value.get("artifacts", [])
    if value.get("artifact_count") != len(rows):
        errors.append("semantic baseline artifact count mismatch")
    for row in rows:
        rel = str(row.get("path", ""))
        target = repo / rel
        if not target.is_file():
            errors.append(f"frozen artifact missing: {rel}")
        elif sha256_file(target) != row.get("sha256"):
            errors.append(f"frozen artifact hash mismatch: {rel}")


def verify_rthp_bindings(repo: Path, receipt: dict[str, Any], errors: list[str]) -> None:
    if receipt.get("status") != "PASS" or receipt.get("failed_test_count") != 0 or receipt.get("error_count") != 0:
        errors.append("RTHP recovery receipt is not clean PASS")
    for relative in RTHP_REGISTRATIONS:
        path = repo / relative
        if not path.is_file():
            errors.append(f"RTHP registration missing: {relative}")
            continue
        document = read_json(path)
        verify_no_authority(document, relative, errors)
        for key, raw in document.items():
            if not isinstance(raw, str) or not key.endswith(("_path", "_root", "_schema")) and key not in {
                "package_root", "feature_catalog", "view_catalog", "cluster_rules", "label_bindings",
                "task_references", "train_activation", "discovery_space", "research_objectives", "source_schema",
            }:
                continue
            if raw.startswith(("http://", "https://", "al://")):
                continue
            if "/" in raw and not (repo / raw).exists():
                errors.append(f"RTHP registration target missing: {relative}: {key}={raw}")

    for root_relative in ACTIVE_RTHP_ROOTS:
        root = repo / root_relative
        if not root.is_dir():
            errors.append(f"active RTHP root missing: {root_relative}")
            continue
        for path in root.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8-sig")
            for forbidden in FORBIDDEN_ACTIVE_PREFIXES:
                if forbidden in text:
                    errors.append(f"active RTHP code contains hardcoded legacy prefix: {path.relative_to(repo)}: {forbidden}")


def verify_release(repo: Path, errors: list[str]) -> None:
    release = repo / RELEASE_ROOT
    required = {
        "README.md", "INSTALL.md", "ROLLBACK.md", "COMMIT_MESSAGE.txt", "APPLY.ps1",
        "PATCH_MANIFEST.json", "PATCH_FILE_INDEX.txt", "PATCH_FILE_HASHES.sha256", "QA_REPORT.json",
    }
    if not release.is_dir():
        errors.append(f"release directory missing: {RELEASE_ROOT.as_posix()}")
        return
    present = {item.name for item in release.iterdir() if item.is_file()}
    missing = sorted(required - present)
    if missing:
        errors.append(f"release controls missing: {missing}")
        return
    index = [line.strip().replace("\\", "/") for line in (release / "PATCH_FILE_INDEX.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
    if index != sorted(set(index)):
        errors.append("patch file index is not sorted and unique")
    for rel in index:
        if not (repo / rel).is_file():
            errors.append(f"patch index target missing: {rel}")
    ledger: dict[str, str] = {}
    for line in (release / "PATCH_FILE_HASHES.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            digest, rel = line.split("  ", 1)
        except ValueError:
            errors.append(f"invalid patch hash line: {line}")
            continue
        ledger[rel.replace("\\", "/")] = "sha256:" + digest.removeprefix("sha256:")
    expected_hashed = set(index) - {f"{RELEASE_ROOT.as_posix()}/PATCH_FILE_HASHES.sha256"}
    if set(ledger) != expected_hashed:
        errors.append("patch hash ledger paths do not match the patch index")
    for rel, expected in ledger.items():
        target = repo / rel
        if target.is_file() and "sha256:" + canonical_sha256(target) != expected:
            errors.append(f"patch hash mismatch: {rel}")
    manifest = read_json(release / "PATCH_MANIFEST.json")
    if manifest.get("patch_file_count") != len(index):
        errors.append("patch manifest file count mismatch")
    verify_no_authority(manifest.get("authority", {}), "release manifest authority", errors)


def verify(repo: Path, *, verify_release_controls: bool = True) -> list[str]:
    repo = RepositoryPaths.discover(repo).root
    errors: list[str] = []

    uc03 = read_json(repo / "registry/consolidation/uc03/part3/part3_exit_decision.json")
    if uc03.get("status") != "ACCEPTED" or uc03.get("uc03_closed") is not True or uc03.get("uc04_authorized") is not True:
        errors.append("UC-03 is not accepted and authorized for UC-04")

    registry: dict[str, dict[str, Any]] = {}
    for name in REQUIRED_REGISTRY:
        path = repo / REGISTRY_ROOT / name
        if not path.is_file():
            errors.append(f"missing UC04-W0 registry document: {name}")
            continue
        try:
            document = read_json(path)
        except Exception as exc:
            errors.append(f"invalid UC04-W0 registry document {name}: {exc}")
            continue
        registry[name] = document
        verify_document_digest(path.relative_to(repo), document, errors)
        verify_no_authority(document, name, errors)

    for name in REQUIRED_SCHEMAS:
        path = repo / SCHEMA_ROOT / name
        if not path.is_file():
            errors.append(f"missing UC04 schema: {name}")
        else:
            try:
                Draft202012Validator.check_schema(read_json(path))
            except Exception as exc:
                errors.append(f"invalid UC04 schema {name}: {exc}")

    if "path_contract.json" in registry and (repo / SCHEMA_ROOT / "path_contract.schema.json").is_file():
        validate_schema(repo / REGISTRY_ROOT / "path_contract.json", repo / SCHEMA_ROOT / "path_contract.schema.json", errors)
        verify_path_contract(repo, registry["path_contract.json"], errors)
    if "w0_exit_decision.json" in registry and (repo / SCHEMA_ROOT / "w0_exit_decision.schema.json").is_file():
        validate_schema(repo / REGISTRY_ROOT / "w0_exit_decision.json", repo / SCHEMA_ROOT / "w0_exit_decision.schema.json", errors)
    if "test_recovery_receipt.json" in registry:
        verify_pytest_contract(repo, registry["test_recovery_receipt.json"], errors)
    for name in ("uc01_static_amendment.json", "uc03_post_closure_amendment.json", "obsidian_foundation_amendment.json"):
        if name in registry:
            verify_amendment(repo / REGISTRY_ROOT / name, registry[name], errors)
    if "semantic_baseline_freeze.json" in registry:
        verify_frozen_baseline(repo, registry["semantic_baseline_freeze.json"], errors)
    if "rthp_recovery_receipt.json" in registry:
        verify_rthp_bindings(repo, registry["rthp_recovery_receipt.json"], errors)

    exit_decision = registry.get("w0_exit_decision.json", {})
    if exit_decision.get("status") != "ACCEPTED" or exit_decision.get("next_wave") != "UC04-W1":
        errors.append("UC04-W0 exit decision is not accepted or does not hand off to UC04-W1")
    candidate = registry.get("first_candidate_registration.json", {})
    if candidate.get("status") != "AUTHORIZED_FOR_CHARACTERIZATION_ONLY" or candidate.get("implementation_authority") is not False:
        errors.append("UC04-W1 candidate authority exceeds characterization-only handoff")
    ledger = registry.get("capability_migration_ledger.json", {})
    if ledger.get("row_count") != len(ledger.get("rows", [])) or ledger.get("row_count") != 0:
        errors.append("UC04-W0 capability ledger must remain empty")

    if verify_release_controls:
        verify_release(repo, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify UC04-W0 semantic-unification foundation and recovery evidence.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--skip-release-controls", action="store_true")
    args = parser.parse_args()
    errors = verify(Path(args.repo_root), verify_release_controls=not args.skip_release_controls)
    print(f"UC04-W0 errors: {len(errors)}")
    for error in errors[:200]:
        print("ERROR:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
