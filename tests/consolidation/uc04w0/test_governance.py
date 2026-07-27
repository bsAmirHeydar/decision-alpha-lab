from __future__ import annotations

import hashlib
import json

from jsonschema import Draft202012Validator

REGISTRY = "registry/consolidation/uc04/w0"


def digest(document, field):
    material = {key: value for key, value in document.items() if key != field}
    payload = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def load(repo_root, relative):
    return json.loads((repo_root / relative).read_text(encoding="utf-8-sig"))


def test_all_w0_registry_documents_are_digest_bound(repo_root):
    for path in sorted((repo_root / REGISTRY).glob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8-sig"))
        field = "amendment_digest" if "amendment_digest" in document else "document_digest"
        assert document[field] == digest(document, field), path


def test_w0_grants_no_destructive_or_execution_authority(repo_root):
    forbidden = {
        "semantic_change", "semantic_merge_authority", "deletion_authority",
        "runtime_authority", "order_authority", "capital_authority",
        "runtime_authority_created", "order_authority_created", "capital_authority_created",
    }
    for path in sorted((repo_root / REGISTRY).glob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8-sig"))
        for key in forbidden:
            assert document.get(key) is not True, (path, key)
        for row in document.get("records", []):
            for key in forbidden:
                assert row.get(key) is not True, (path, row, key)


def test_path_and_exit_documents_validate_against_schemas(repo_root):
    pairs = (
        ("path_contract.json", "path_contract.schema.json"),
        ("w0_exit_decision.json", "w0_exit_decision.schema.json"),
    )
    for document_name, schema_name in pairs:
        document = load(repo_root, f"{REGISTRY}/{document_name}")
        schema = load(repo_root, f"schemas/consolidation/uc04/{schema_name}")
        Draft202012Validator(schema).validate(document)


def test_w0_ledger_is_empty_and_w1_is_characterization_only(repo_root):
    ledger = load(repo_root, f"{REGISTRY}/capability_migration_ledger.json")
    candidate = load(repo_root, f"{REGISTRY}/first_candidate_registration.json")
    assert ledger["rows"] == [] and ledger["row_count"] == 0
    assert candidate["status"] == "AUTHORIZED_FOR_CHARACTERIZATION_ONLY"
    assert candidate["implementation_authority"] is False
    assert candidate["consumer_cutover_authority"] is False


def test_full_suite_limitation_is_explicit_and_not_reported_as_pass(repo_root):
    receipt = load(repo_root, f"{REGISTRY}/test_recovery_receipt.json")
    attempt = receipt["full_repository_suite_attempt"]
    assert attempt["status"] == "INCOMPLETE_AT_FIRST_HISTORICAL_LFS_BLOCKER"
    assert attempt["source_archive_bytes_unchanged"] is True
    assert attempt["unresolved_beyond_first_blocker"] is True
    assert len(attempt["git_lfs_pointer_paths"]) == 4
