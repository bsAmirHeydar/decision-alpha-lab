from __future__ import annotations
import pytest
from tools.strategy_factory.acl_os.acl_00.catalogs import PolicyBundle


def test_every_approval_role_is_registered():
    bundle=PolicyBundle.load(); roles=set(bundle.documents["authority_roles"]["roles"])
    referenced={role for policy in bundle.documents["approval_policy"]["policies"].values() for role in policy.get("required_roles",{})}
    assert referenced <= roles


def test_every_action_capability_is_grantable():
    bundle=PolicyBundle.load(); granted={cap for role in bundle.documents["authority_roles"]["roles"].values() for cap in role.get("capabilities",[])}
    requested={cap for action in bundle.documents["action_catalog"]["actions"].values() for cap in action.get("required_capabilities",[])}
    assert requested <= granted


def test_every_transition_requester_capability_is_grantable():
    bundle=PolicyBundle.load(); granted={cap for role in bundle.documents["authority_roles"]["roles"].values() for cap in role.get("capabilities",[])}
    requested={cap for transition in bundle.documents["lifecycle_transitions"]["transitions"].values() for cap in transition.get("requester_capabilities",[])}
    assert requested <= granted


def test_adjacent_primary_lifecycle_is_complete():
    bundle=PolicyBundle.load(); registered=set(bundle.documents["lifecycle_transitions"]["transitions"])
    states=["DRAFT_CONTEXT","SEMANTICALLY_VALIDATED","CONTEXT_COMPILED","REPLAY_VALIDATED","OCCURRENCE_DATASET_READY","SETUP_UNIVERSE_READY","BATCH_REGISTERED","RESEARCH_RUNNING","EVIDENCE_COMPLETE","STATISTICALLY_ELIGIBLE","RUNTIME_COMPATIBLE","PAPER_CHALLENGER","SHADOW_CHALLENGER","MICRO_LIVE_ELIGIBLE","CHAMPION"]
    assert all(f"{a}->{b}" in registered for a,b in zip(states,states[1:]))


def test_retired_has_no_outgoing_transition():
    registered=PolicyBundle.load().documents["lifecycle_transitions"]["transitions"]
    assert not any(key.startswith("RETIRED->") for key in registered)

@pytest.mark.parametrize("profile",["base","research","runtime","capital"])
def test_security_profiles_are_monotonic(profile):
    policies=PolicyBundle.load().documents["security_hook_policy"]["policies"]
    base=set(policies["base"]["required_controls"])
    assert base <= set(policies[profile]["required_controls"])


def test_capital_controls_include_kill_switch_and_isolation():
    controls=set(PolicyBundle.load().documents["security_hook_policy"]["policies"]["capital"]["required_controls"])
    assert {"SEC_KEY_CUSTODY","SEC_KILL_SWITCH","SEC_CAPITAL_ISOLATION"} <= controls


def test_claim_policy_hard_disables_live_authority():
    policy=PolicyBundle.load().documents["claim_ceiling_bindings"]
    assert policy["capital_activation_allowed"] is False
    assert policy["live_order_submission_allowed"] is False
