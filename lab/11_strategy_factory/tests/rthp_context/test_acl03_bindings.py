
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BINDINGS = ROOT / "lab/11_strategy_factory/contexts/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1/generated/acl_03/bindings"


def load(name):
    return json.loads((BINDINGS / name).read_text(encoding="utf-8"))


def test_saed_binding_is_seed_only():
    value = load("rthp_saed_binding.json")
    assert value["implementation_status"] == "CONTRACT_AND_SEED_READY"
    assert "TRAIN_MODEL" in value["forbidden_operations"]
    assert value["live_order_submission_allowed"] is False
    assert value["capital_activation_allowed"] is False


def test_ucee_binding_blocks_training_until_acl05():
    value = load("rthp_ucee_binding.json")
    assert value["research_entry_ready"] is False
    assert "ACL05_IMMUTABLE_BATCH_REQUIRED" in value["research_entry_blockers"]
    assert "TRAIN_BEFORE_ACL05" in value["forbidden_operations"]


def test_twin_seed_is_semantically_immutable():
    value = load("rthp_context_twin_seed.json")
    assert value["immutable_semantics"] is True
    assert value["learning_authority_created"] is False
    assert value["treatment_authority_created"] is False
