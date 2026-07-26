from __future__ import annotations
import pytest
from src.engine.tooling.strategy_factory.acl_os.acl_00.authority import AuthorityEvaluator
from src.engine.tooling.strategy_factory.acl_os.acl_00.catalogs import PolicyBundle
from src.engine.tooling.strategy_factory.acl_os.acl_00.types import Actor

@pytest.fixture
def evaluator(): return AuthorityEvaluator(PolicyBundle.load())

def actor(*roles,tenant="TEN_ALPHA",strength="MFA"): return Actor("USR_TEST",tuple(roles),tenant,strength)

@pytest.mark.parametrize("role,capability",[("CONTEXT_OWNER","PROPOSE_TRANSITION"),("DOCTRINE_REVIEWER","APPROVE_SEMANTICS"),("SECURITY_REVIEWER","SUSPEND"),("CAPITAL_AUTHORITY","APPROVE_MICRO_LIVE"),("AUDITOR","READ_AUDIT")])
def test_role_capability_mapping(evaluator,role,capability): assert capability in evaluator.capabilities(actor(role))

def test_unknown_role_has_no_capability(evaluator): assert evaluator.capabilities(actor("UNKNOWN"))==set()

def test_tenant_mismatch_fails(evaluator):
    policy={"requester_capabilities":["PROPOSE_TRANSITION"]}; reasons=evaluator.evaluate_requester(actor("CONTEXT_OWNER",tenant="TEN_OTHER"),policy,"TEN_ALPHA"); assert any(x.code=="TENANT_MISMATCH" for x in reasons)

def test_weak_authentication_fails(evaluator):
    reasons=evaluator.evaluate_requester(actor("CONTEXT_OWNER",strength="PASSWORD"),{"requester_capabilities":["PROPOSE_TRANSITION"]},"TEN_ALPHA"); assert any(x.code=="AUTHENTICATION_TOO_WEAK" for x in reasons)

def test_allowed_actions_are_state_and_capability_bounded(evaluator):
    assert "EDIT_CONTEXT" in evaluator.allowed_actions(actor("CONTEXT_OWNER"),"DRAFT_CONTEXT")
    assert "READ_AUDIT" not in evaluator.allowed_actions(actor("CONTEXT_OWNER"),"DRAFT_CONTEXT")
