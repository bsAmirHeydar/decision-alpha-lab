import pytest
from src.engine.tooling.strategy_factory.lcm.lcm_07.authority import build_permit,verify_permit
from src.engine.tooling.strategy_factory.lcm.lcm_07.errors import PolicyError

def test_permit_denies_all_mutation():
 p=build_permit("sha256:"+"1"*64,"FRAMEWORK_X","2026-07-19T00:00:00Z");assert verify_permit(p,p["source_handoff_digest"],"FRAMEWORK_X")
 for k in ("source_move_allowed","source_delete_allowed","target_materialization_allowed","merge_allowed","runtime_authority","live_order_authority","capital_authority"):assert p[k] is False
def test_tampered_permit_fails():
 p=build_permit("sha256:"+"1"*64,"FRAMEWORK_X","2026-07-19T00:00:00Z");p["merge_allowed"]=True
 with pytest.raises(PolicyError):verify_permit(p,p["source_handoff_digest"],"FRAMEWORK_X")
