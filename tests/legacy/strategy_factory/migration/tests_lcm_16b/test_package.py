import json

from src.engine.tooling.strategy_factory.lcm.lcm_16b.constants import PHASE_SEQUENCE, UPSTREAM_HANDOFF_DIGEST
from src.engine.tooling.strategy_factory.lcm.lcm_16b.io import load_json, load_jsonl
from src.engine.tooling.strategy_factory.lcm.lcm_16b.verify import verify_program_closure_package


def test_package_verifies(repo_root, package_root):
    result = verify_program_closure_package(repo_root, package_root)
    assert result.validation_status == "PASS"
    assert result.program_closure_decision == "BLOCKED"


def test_upstream_binding_is_exact(package_root):
    binding = load_json(package_root / "upstream_binding.json")
    assert binding["upstream_handoff_digest"] == UPSTREAM_HANDOFF_DIGEST
    assert binding["upstream_closure_decision"] == "BLOCKED"


def test_phase_register_is_complete(package_root):
    rows = load_jsonl(package_root / "records/phase_register.jsonl")
    assert [row["phase_id"] for row in rows] == list(PHASE_SEQUENCE)
    assert len(rows) == 30


def test_package_json_is_parseable(package_root):
    for path in package_root.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))


def test_certificate_not_overissued(package_root):
    certificate = load_json(package_root / "program_closure_certificate.json")
    assert certificate["certificate_status"] == "NOT_ISSUED"
    assert certificate["claim"] == "NO_PROGRAM_CLOSURE_CLAIM"
