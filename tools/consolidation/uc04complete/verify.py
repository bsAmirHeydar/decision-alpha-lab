from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from tools.consolidation.uc04complete.build import (
    CAPABILITIES,
    REGISTRY_ROOT,
    SCHEMA_ROOT,
    SELF_TEST,
    build_records,
    document_digest,
)
from tools.consolidation.uc04w0.verify import verify as verify_w0
from tools.consolidation.uc04w1.verify import verify as verify_w1
from tools.consolidation.uc04w1b.verify import verify as verify_w1b
from tools.consolidation.uc04w1bn1.verify import verify as verify_w1bn1
from tools.repository_paths import RepositoryPaths

RELEASE_ROOT = Path("releases/unified_consolidation/uc04/complete")

REQUIRED_RECORDS = (
    "capability_implementation_ledger.json",
    "explicit_variant_registry.json",
    "logic_preservation_certificates.json",
    "native_acceptance_contract.json",
    "w1_candidate_transition.json",
    "uc04_exit_decision.json",
)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"object expected: {path}")
    return value



def _validate_optional_acceptance(root: Path, errors: list[str]) -> None:
    acceptance_path = root / REGISTRY_ROOT / "uc04_acceptance.json"
    handoff_path = root / REGISTRY_ROOT / "uc05_handoff_decision.json"
    if acceptance_path.exists() != handoff_path.exists():
        errors.append("UC04 acceptance and UC05 handoff records must appear together")
        return
    if not acceptance_path.exists():
        return
    for path, schema_name in (
        (acceptance_path, "uc04_acceptance.schema.json"),
        (handoff_path, "uc05_handoff_decision.schema.json"),
    ):
        try:
            value = read_json(path)
            if value.get("document_digest") != document_digest(value):
                errors.append(f"document digest mismatch: {path.name}")
            schema = read_json(root / SCHEMA_ROOT / schema_name)
            Draft202012Validator.check_schema(schema)
            for issue in Draft202012Validator(schema).iter_errors(value):
                location = "/".join(str(part) for part in issue.path) or "<root>"
                errors.append(f"schema violation {path.name}@{location}: {issue.message}")
        except Exception as exc:
            errors.append(f"invalid optional acceptance record {path.name}: {exc}")


def _verify_release(root: Path, errors: list[str]) -> None:
    release = root / RELEASE_ROOT
    required = {
        "APPLY.ps1", "README.md", "INSTALL.md", "ROLLBACK.md", "COMMIT_MESSAGE.txt",
        "PATCH_FILE_INDEX.txt", "PATCH_FILE_HASHES.sha256", "PATCH_MANIFEST.json", "QA_REPORT.json",
    }
    if not release.is_dir():
        errors.append("UC04 complete release directory is missing")
        return
    present = {path.name for path in release.iterdir() if path.is_file()}
    if required - present:
        errors.append(f"UC04 complete release controls missing: {sorted(required - present)}")
        return
    index = [line.strip().replace("\\", "/") for line in (release / "PATCH_FILE_INDEX.txt").read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if index != sorted(set(index)):
        errors.append("UC04 complete patch index is not sorted and unique")
    forbidden_parts = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}
    for relative in index:
        parts = Path(relative).parts
        if relative.startswith("/") or ".." in parts or any(part in forbidden_parts for part in parts):
            errors.append(f"unsafe UC04 complete patch path: {relative}")
        target = root / relative
        if not target.is_file():
            errors.append(f"UC04 complete indexed path missing: {relative}")
        elif target.read_bytes().startswith(b"version https://git-lfs.github.com/spec/v1\n"):
            errors.append(f"UC04 complete patch contains Git LFS pointer: {relative}")
    ledger: dict[str, str] = {}
    for line in (release / "PATCH_FILE_HASHES.sha256").read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        try:
            digest, relative = line.split("  ", 1)
        except ValueError:
            errors.append(f"invalid UC04 complete hash row: {line}")
            continue
        ledger[relative.replace("\\", "/")] = digest.lower()
    hash_relative = f"{RELEASE_ROOT.as_posix()}/PATCH_FILE_HASHES.sha256"
    if set(ledger) != set(index) - {hash_relative}:
        errors.append("UC04 complete hash ledger membership mismatch")
    import hashlib
    for relative, expected in ledger.items():
        target = root / relative
        if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            errors.append(f"UC04 complete patch hash mismatch: {relative}")
    for name, schema_name in (("PATCH_MANIFEST.json", "patch_manifest.schema.json"), ("QA_REPORT.json", "qa_report.schema.json")):
        path = release / name
        try:
            value = read_json(path)
            if value.get("document_digest") != document_digest(value):
                errors.append(f"document digest mismatch: {name}")
            schema = read_json(root / SCHEMA_ROOT / schema_name)
            Draft202012Validator.check_schema(schema)
            for issue in Draft202012Validator(schema).iter_errors(value):
                location = "/".join(str(part) for part in issue.path) or "<root>"
                errors.append(f"schema violation {name}@{location}: {issue.message}")
        except Exception as exc:
            errors.append(f"invalid UC04 complete release record {name}: {exc}")
    if (release / "APPLY.ps1").is_file():
        apply_text = (release / "APPLY.ps1").read_text(encoding="utf-8-sig").lower()
        for forbidden in ("git add .", "git add -a", "git commit", "git push"):
            if forbidden in apply_text:
                errors.append(f"UC04 complete installer contains forbidden Git action: {forbidden}")


def verify(repo: Path, *, include_upstream: bool = True) -> list[str]:
    root = RepositoryPaths.discover(repo).root
    errors: list[str] = []
    if include_upstream:
        for label, function in (
            ("UC04-W0", verify_w0),
            ("UC04-W1", verify_w1),
            ("UC04-W1B", verify_w1b),
            ("UC04-W1B-N1", verify_w1bn1),
        ):
            for error in function(root):
                errors.append(f"{label}: {error}")

    expected = build_records(root)
    for name in REQUIRED_RECORDS:
        path = root / REGISTRY_ROOT / name
        if not path.is_file():
            errors.append(f"missing UC04 complete record: {name}")
            continue
        try:
            value = read_json(path)
        except Exception as exc:
            errors.append(f"invalid UC04 complete record {name}: {exc}")
            continue
        if value.get("document_digest") != document_digest(value):
            errors.append(f"document digest mismatch: {name}")
        if value != expected[name]:
            errors.append(f"record is not reproducible: {name}")
        schema_name = Path(str(value.get("$schema", ""))).name
        schema_path = root / SCHEMA_ROOT / schema_name
        if not schema_path.is_file():
            errors.append(f"missing schema for {name}: {schema_name}")
        else:
            try:
                schema = read_json(schema_path)
                Draft202012Validator.check_schema(schema)
                for issue in Draft202012Validator(schema).iter_errors(value):
                    location = "/".join(str(part) for part in issue.path) or "<root>"
                    errors.append(f"schema violation {name}@{location}: {issue.message}")
            except Exception as exc:
                errors.append(f"schema validation failed {name}: {exc}")

    ledger = expected["capability_implementation_ledger.json"]
    if ledger.get("selected_capability_count") != 14:
        errors.append("selected shared capability count must be 14")
    if ledger.get("consumer_adapter_count") != 109:
        errors.append("consumer adapter count must be 109")
    variants = expected["explicit_variant_registry.json"]
    if variants.get("historical_candidate_count") != 205 or variants.get("explicit_variant_count") != 191:
        errors.append("historical candidate partition must be 14 shared + 191 explicit variants")

    for spec in CAPABILITIES:
        include = root / spec["include"]
        if not include.is_file():
            errors.append(f"canonical include missing: {spec['include']}")
            continue
        text = include.read_text(encoding="utf-8-sig")
        if not re.search(r"\b" + re.escape(spec["function"]) + r"\s*\(", text):
            errors.append(f"canonical function missing: {spec['function']}")
        if "RTHP" in text or "CTX_RTHP" in text:
            errors.append(f"context-specific branch in shared kernel: {spec['include']}")

    for capability in ledger.get("capabilities", []):
        token = next(item["adapter_token"] for item in CAPABILITIES if item["candidate_id"] == capability["candidate_id"])
        for member in capability.get("members", []):
            path = root / member["artifact_path"]
            if not path.is_file():
                errors.append(f"consumer missing: {member['artifact_path']}")
                continue
            if token not in path.read_text(encoding="utf-8-sig"):
                errors.append(f"consumer adapter missing: {member['artifact_path']}:{member['function_name']}")

    if not (root / SELF_TEST).is_file():
        errors.append("native phase self-test missing")
    else:
        text = (root / SELF_TEST).read_text(encoding="utf-8-sig")
        for token in (
            "UC04_SELFTEST_SUMMARY",
            "AL_UC04FormatDateTime",
            "AL_UC04CreateArrow",
            "AL_UC04BuildM0001Config",
            "AL_UC04BuildM0002Config",
            "AL_UC04BuildDayeTimeConfig",
            "AL_UC04UpdateLiveBarStream",
        ):
            if token not in text:
                errors.append(f"native self-test missing coverage token: {token}")
        for forbidden in ("OrderSend", "CTrade", "PositionOpen", "WebRequest"):
            if forbidden in text:
                errors.append(f"native self-test has forbidden authority: {forbidden}")

    exit_record = expected["uc04_exit_decision.json"]
    if exit_record.get("implementation_status") != "COMPLETE":
        errors.append("UC04 implementation is not complete")
    if exit_record.get("uc05_handoff_authorized") is not False:
        errors.append("UC05 handoff cannot be authorized before native seal")
    for field in ("deletion_authority", "runtime_authority", "order_authority", "capital_authority"):
        if exit_record.get(field) is not False:
            errors.append(f"forbidden authority in UC04 exit record: {field}")
    _validate_optional_acceptance(root, errors)
    _verify_release(root, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify complete UC-04 semantic unification implementation.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--skip-upstream", action="store_true")
    args = parser.parse_args()
    errors = verify(Path(args.repo_root), include_upstream=not args.skip_upstream)
    if errors:
        print(f"UC04 complete errors: {len(errors)}")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("UC04 complete verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
