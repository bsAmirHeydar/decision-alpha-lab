from tools.strategy_factory.lcm.lcm_16b.closure import evaluate_program_closure, run_policy_replay
from tools.strategy_factory.lcm.lcm_16b.constants import REQUIRED_EXTERNAL_DIMENSIONS
from tools.strategy_factory.lcm.lcm_16b.io import load_json


def _recovery():
    return {"local_control_plane_status": "PASS", "lcm16a_rehydration_status": "PASS", "receipt_digest": "sha256:" + "1" * 64}


def _evidence(status="PASS", approval="PASS"):
    return {
        "dimensions": [{"dimension": item, "status": status, "evidence_digest": "sha256:" + "2" * 64} for item in REQUIRED_EXTERNAL_DIMENSIONS],
        "approval_status": approval,
        "approvals": [{"evidence_digest": "sha256:" + "3" * 64}],
    }


def test_unknown_gate_blocks():
    decision, certificate = evaluate_program_closure(_recovery(), _evidence("UNKNOWN", "BLOCKED"))
    assert decision["decision"] == "BLOCKED"
    assert certificate["certificate_status"] == "NOT_ISSUED"


def test_failed_gate_fails():
    decision, _ = evaluate_program_closure(_recovery(), _evidence("FAILED"))
    assert decision["decision"] == "FAILED"


def test_all_pass_with_approvals_accepts():
    decision, certificate = evaluate_program_closure(_recovery(), _evidence())
    assert decision["decision"] == "ACCEPTED"
    assert certificate["certificate_status"] == "ISSUED"


def test_all_pass_without_approval_blocks():
    decision, _ = evaluate_program_closure(_recovery(), _evidence("PASS", "BLOCKED"))
    assert decision["decision"] == "BLOCKED"


def test_policy_replay_covers_both_sides():
    report = run_policy_replay()
    assert report["negative_unknown_replay_decision"] == "BLOCKED"
    assert report["all_pass_replay_decision"] == "ACCEPTED"
