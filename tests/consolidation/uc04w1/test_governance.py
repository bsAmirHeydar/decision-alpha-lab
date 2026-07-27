from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.consolidation.uc04w1.characterize import REGISTRY_ROOT, canonical_digest, characterize
from tools.consolidation.uc04w1.verify import REQUIRED_RECORDS, REQUIRED_SCHEMAS


def test_all_records_are_reproducible_schema_valid_and_hash_bound(repo_root: Path) -> None:
    expected = characterize(repo_root)
    for name in REQUIRED_RECORDS:
        path = repo_root / REGISTRY_ROOT / name
        actual = json.loads(path.read_text())
        assert actual == expected[name]
        assert actual["document_digest"] == canonical_digest(actual)
        schema = json.loads((repo_root / "schemas/consolidation/uc04/w1" / Path(actual["$schema"]).name).read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(actual)


def test_schema_set_is_complete(repo_root: Path) -> None:
    for name in REQUIRED_SCHEMAS:
        assert (repo_root / "schemas/consolidation/uc04/w1" / name).is_file()


def test_w1a_native_and_cutover_authority_remain_blocked(repo_root: Path) -> None:
    exit_decision = json.loads((repo_root / REGISTRY_ROOT / "w1a_exit_decision.json").read_text())
    certificate = json.loads((repo_root / REGISTRY_ROOT / "logic_preservation_certificate.json").read_text())
    assert exit_decision["status"] == "CHARACTERIZATION_ACCEPTED_IMPLEMENTATION_BLOCKED"
    assert exit_decision["native_compile_status"] == "PENDING_LOCAL_WINDOWS"
    assert exit_decision["native_runtime_status"] == "PENDING_LOCAL_WINDOWS"
    assert certificate["status"] == "BLOCKED_PENDING_NATIVE_EVIDENCE"
    assert certificate["native_evidence"] == []
