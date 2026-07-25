from dataclasses import replace
import pytest
from strategy_factory_policy_v3.golden import *
from strategy_factory_policy_v3.fallback import fallback_resolution
from strategy_factory_policy_v3.authority import resolve_hard_authority
from strategy_factory_policy_v3.manual import evaluate_manual
from strategy_factory_policy_v3.enums import *
from strategy_factory_policy_v3.contracts import OperatorOverride
from strategy_factory_policy_v3.errors import PolicyError

def test_invalid_model_maps_manual_only(): assert golden_fallback().action_for(FallbackReason.INVALID_MODEL) is FallbackAction.MANUAL_ONLY
def test_conflict_maps_abstain(): assert golden_fallback().action_for(FallbackReason.CONFLICT) is FallbackAction.ABSTAIN
def test_risk_maps_reject(): assert golden_fallback().action_for(FallbackReason.RISK_REJECTION) is FallbackAction.REJECT
def test_manual_fallback_preserves_manual_action():
    m=evaluate_manual(golden_manual(),golden_occurrence()); r=fallback_resolution(golden_fallback(),FallbackReason.INVALID_MODEL,m); assert r[1] is Action.ENTER_LONG and r[2]=='market'
def test_kill_switch_precedence(): assert resolve_hard_authority(kill_switch=True,risk_rejected=True,manual_veto=True,override=None,known_time_ms=1)[1] is Authority.KILL_SWITCH
def test_risk_precedence_over_manual(): assert resolve_hard_authority(kill_switch=False,risk_rejected=True,manual_veto=True,override=None,known_time_ms=1)[1] is Authority.RISK_ENGINE
def test_expired_override_rejected():
    ov=OperatorOverride('ov','occ:1',OverrideKind.APPROVE,'op','ok',1,2,'a'*64)
    with pytest.raises(PolicyError):resolve_hard_authority(kill_switch=False,risk_rejected=False,manual_veto=False,override=ov,known_time_ms=3)
