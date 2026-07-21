
import json
from pathlib import Path

from tools.strategy_factory.contexts.rthp.acl03_bindings import validate_rthp_acl03_bundle

ROOT = Path(__file__).resolve().parents[4]
PKG = ROOT / "lab/11_strategy_factory/contexts/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1"
COMPILED = PKG / "generated/acl_03/compiled"
BINDINGS = PKG / "generated/acl_03/bindings"


def test_committed_acl03_bundle_is_valid():
    result = validate_rthp_acl03_bundle(PKG, COMPILED, BINDINGS)
    assert result["passed"], result
    assert result["highest_state"] == "CONTEXT_COMPILED"
    assert result["compiled_case_count"] == 12


def test_acl03_handoff_is_bounded():
    handoff = json.loads((COMPILED / "handoff/acl04_handoff.json").read_text(encoding="utf-8"))
    assert handoff["search_authority_required"] is True
    assert handoff["live_order_submission_allowed"] is False
    assert handoff["capital_activation_allowed"] is False
    assert "ALTER_CONTEXT_SEMANTICS" in handoff["forbidden_scope"]
