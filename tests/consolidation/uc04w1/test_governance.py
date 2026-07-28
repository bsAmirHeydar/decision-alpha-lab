from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.consolidation.uc04w1.characterize import REGISTRY_ROOT, canonical_digest, characterize
from tools.consolidation.uc04w1.verify import REQUIRED_RECORDS, REQUIRED_SCHEMAS, verify_complete_transition


def test_all_records_are_valid_historical_evidence_or_reproducible(repo_root: Path) -> None:
    transition_errors: list[str] = []
    transition = verify_complete_transition(repo_root, transition_errors)
    assert transition_errors == []
    expected = characterize(repo_root) if transition is None else {}
    for name in REQUIRED_RECORDS:
        path = repo_root / REGISTRY_ROOT / name
        actual = json.loads(path.read_text())
        if transition is None:
            assert actual == expected[name]
        assert actual["document_digest"] == canonical_digest(actual)
        schema = json.loads((repo_root / "schemas/consolidation/uc04/w1" / Path(actual["$schema"]).name).read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(actual)


def test_schema_set_is_complete(repo_root: Path) -> None:
    for name in REQUIRED_SCHEMAS:
        assert (repo_root / "schemas/consolidation/uc04/w1" / name).is_file()


def test_w1a_historical_authority_remains_blocked(repo_root: Path) -> None:
    exit_decision = json.loads((repo_root / REGISTRY_ROOT / "w1a_exit_decision.json").read_text())
    certificate = json.loads((repo_root / REGISTRY_ROOT / "logic_preservation_certificate.json").read_text())
    assert exit_decision["status"] == "CHARACTERIZATION_ACCEPTED_IMPLEMENTATION_BLOCKED"
    assert certificate["status"] == "BLOCKED_PENDING_NATIVE_EVIDENCE"
    assert certificate["native_evidence"] == []
