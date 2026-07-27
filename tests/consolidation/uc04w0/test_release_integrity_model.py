from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.consolidation.release_integrity import verify_historical_release_snapshot

RELEASE_ROOT = Path("releases/unified_consolidation/uc04/w0")
POLICY_PATH = Path("registry/consolidation/release_integrity/policy_v1.json")
POLICY_SCHEMA = Path("schemas/consolidation/release_integrity/policy.schema.json")
AMENDMENT_SCHEMA = Path("schemas/consolidation/release_integrity/amendment.schema.json")


def _digest_document(value: dict, field: str = "document_digest") -> str:
    payload = json.dumps(
        {key: item for key, item in value.items() if key != field},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _build_minimal_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    release = repo / RELEASE_ROOT
    release.mkdir(parents=True)
    active = repo / "tools/active.py"
    active.parent.mkdir(parents=True)
    active.write_text("VALUE = 1\n", encoding="utf-8")

    controls = {
        "README.md": b"release readme\n",
        "INSTALL.md": b"install\n",
        "ROLLBACK.md": b"rollback\n",
        "COMMIT_MESSAGE.txt": b"test release\n",
        "APPLY.ps1": b"Write-Host 'apply'\n",
        "QA_REPORT.json": b"{}\n",
    }
    for name, payload in controls.items():
        (release / name).write_bytes(payload)

    index = sorted(
        [
            *(f"{RELEASE_ROOT.as_posix()}/{name}" for name in controls),
            f"{RELEASE_ROOT.as_posix()}/PATCH_FILE_HASHES.sha256",
            f"{RELEASE_ROOT.as_posix()}/PATCH_FILE_INDEX.txt",
            f"{RELEASE_ROOT.as_posix()}/PATCH_MANIFEST.json",
            "tools/active.py",
        ]
    )
    (release / "PATCH_FILE_INDEX.txt").write_text("\n".join(index) + "\n", encoding="utf-8")
    manifest = {
        "patch_file_count": len(index),
        "authority": {
            "semantic_change": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
        },
    }
    _write_json(release / "PATCH_MANIFEST.json", manifest)

    ledger_lines: list[str] = []
    for relative in index:
        if relative == f"{RELEASE_ROOT.as_posix()}/PATCH_FILE_HASHES.sha256":
            continue
        ledger_lines.append(f"{_sha((repo / relative).read_bytes())}  {relative}")
    (release / "PATCH_FILE_HASHES.sha256").write_text(
        "\n".join(ledger_lines) + "\n", encoding="utf-8"
    )

    source_schemas = Path(__file__).resolve().parents[3] / "schemas/consolidation/release_integrity"
    for source in source_schemas.glob("*.json"):
        target = repo / "schemas/consolidation/release_integrity" / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())

    policy = {
        "$schema": "../../../schemas/consolidation/release_integrity/policy.schema.json",
        "schema_version": "1.0.0",
        "policy_id": "UC04_HISTORICAL_RELEASE_INTEGRITY_POLICY_V1",
        "program_id": "UCPS",
        "historical_stage": "UC04-W0",
        "status": "ACTIVE",
        "historical_release_semantics": "AUDIT_SNAPSHOT_NOT_PERMANENT_ACTIVE_SOURCE_LOCK",
        "immutable_prefixes": [f"{RELEASE_ROOT.as_posix()}/"],
        "immutable_exact_paths": [],
        "amendment_search_roots": ["registry/consolidation/release_integrity/amendments"],
        "legacy_amendment_documents": [],
        "require_all_index_targets": True,
        "semantic_change": False,
        "runtime_authority_created": False,
        "order_authority_created": False,
        "capital_authority_created": False,
    }
    policy["document_digest"] = _digest_document(policy)
    _write_json(repo / POLICY_PATH, policy)
    return repo


def _verify(repo: Path) -> list[str]:
    return verify_historical_release_snapshot(
        repo,
        release_root=RELEASE_ROOT,
        policy_path=POLICY_PATH,
        policy_schema_path=POLICY_SCHEMA,
        amendment_schema_path=AMENDMENT_SCHEMA,
    )


def test_historical_snapshot_accepts_crlf_checkout_for_immutable_text(tmp_path: Path) -> None:
    repo = _build_minimal_repo(tmp_path)
    apply_path = repo / RELEASE_ROOT / "APPLY.ps1"
    apply_path.write_bytes(apply_path.read_bytes().replace(b"\n", b"\r\n"))
    assert _verify(repo) == []


def test_active_implementation_can_evolve_without_rewriting_historical_ledger(tmp_path: Path) -> None:
    repo = _build_minimal_repo(tmp_path)
    (repo / "tools/active.py").write_text("VALUE = 2\n", encoding="utf-8")
    assert _verify(repo) == []


def test_immutable_release_control_mutation_fails_closed(tmp_path: Path) -> None:
    repo = _build_minimal_repo(tmp_path)
    (repo / RELEASE_ROOT / "README.md").write_text("tampered\n", encoding="utf-8")
    errors = _verify(repo)
    assert f"immutable release artifact hash mismatch: {RELEASE_ROOT.as_posix()}/README.md" in errors


def test_generic_amendment_chain_accepts_reviewed_immutable_correction(tmp_path: Path) -> None:
    repo = _build_minimal_repo(tmp_path)
    relative = f"{RELEASE_ROOT.as_posix()}/README.md"
    target = repo / relative
    previous = "sha256:" + _sha(target.read_bytes())
    target.write_text("reviewed correction\n", encoding="utf-8")
    current = "sha256:" + _sha(target.read_bytes())
    amendment = {
        "$schema": "../../../../schemas/consolidation/release_integrity/amendment.schema.json",
        "schema_version": "1.0.0",
        "amendment_id": "TEST_IMMUTABLE_CORRECTION_01",
        "program_id": "UCPS",
        "upstream_stage": "UC04-W0",
        "status": "PASS",
        "reason": "Test the append-only generic amendment chain.",
        "record_count": 1,
        "records": [
            {
                "path": relative,
                "previous_sha256": previous,
                "current_sha256": current,
                "change_class": "TEST_ONLY",
                "semantic_change": False,
                "runtime_authority_created": False,
                "order_authority_created": False,
                "capital_authority_created": False,
            }
        ],
        "semantic_change": False,
        "runtime_authority_created": False,
        "order_authority_created": False,
        "capital_authority_created": False,
    }
    amendment["document_digest"] = _digest_document(amendment)
    _write_json(
        repo / "registry/consolidation/release_integrity/amendments/test_01.json",
        amendment,
    )
    assert _verify(repo) == []


def test_active_source_amendment_does_not_become_a_new_permanent_lock(tmp_path: Path) -> None:
    repo = _build_minimal_repo(tmp_path)
    relative = "tools/active.py"
    target = repo / relative
    previous = "sha256:" + _sha(target.read_bytes())
    target.write_text("VALUE = 2\n", encoding="utf-8")
    amended = "sha256:" + _sha(target.read_bytes())
    amendment = {
        "$schema": "../../../../schemas/consolidation/release_integrity/amendment.schema.json",
        "schema_version": "1.0.0",
        "amendment_id": "TEST_ACTIVE_CORRECTION_01",
        "program_id": "UCPS",
        "upstream_stage": "UC04-W0",
        "status": "PASS",
        "reason": "Record a historical active-source correction without permanently pinning it.",
        "record_count": 1,
        "records": [
            {
                "path": relative,
                "previous_sha256": previous,
                "current_sha256": amended,
                "change_class": "TEST_ONLY",
                "semantic_change": False,
                "runtime_authority_created": False,
                "order_authority_created": False,
                "capital_authority_created": False,
            }
        ],
        "semantic_change": False,
        "runtime_authority_created": False,
        "order_authority_created": False,
        "capital_authority_created": False,
    }
    amendment["document_digest"] = _digest_document(amendment)
    _write_json(
        repo / "registry/consolidation/release_integrity/amendments/test_active_01.json",
        amendment,
    )
    target.write_text("VALUE = 3\n", encoding="utf-8")
    assert _verify(repo) == []
