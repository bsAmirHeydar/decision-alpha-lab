import pytest
from saed_v4_constitution.authority import AuthorityMatrix
from saed_v4_constitution.enums import ActorType, Authority, DecisionStatus, ReasonCode
from saed_v4_constitution.models import Actor, AuthorityRequest

@pytest.mark.parametrize("authority", [Authority.RESEARCH_PROPOSAL, Authority.SANDBOX_COMPUTE, Authority.EVIDENCE_PACKET_DRAFT, Authority.RED_TEAM_CHALLENGE])
def test_agent_allowed_research_authorities(agent, authority):
    req=AuthorityRequest("p",agent,authority,"2026-07-13T00:00:00Z","research")
    assert AuthorityMatrix().evaluate(req).status == DecisionStatus.ALLOW

@pytest.mark.parametrize("authority", [Authority.ORDER,Authority.BROKER,Authority.NETWORK,Authority.RISK_LIMIT_CHANGE,Authority.PORTFOLIO_ALLOCATION,Authority.RUNTIME_ACTIVATION,Authority.PROMOTION_SIGNATURE,Authority.CONTEXT_TRUTH_MUTATION,Authority.EVIDENCE_ROLE_REASSIGNMENT,Authority.CONSTITUTION_SELF_AMENDMENT,Authority.HIDDEN_EVALUATION_ROW_ACCESS])
def test_agent_hard_denied(agent, authority):
    req=AuthorityRequest("p",agent,authority,"2026-07-13T00:00:00Z","research")
    result=AuthorityMatrix().evaluate(req)
    assert result.status == DecisionStatus.REJECT
    assert ReasonCode.AUTHORITY_DENIED in result.reasons

def test_researcher_cannot_order(researcher):
    req=AuthorityRequest("p",researcher,Authority.ORDER,"2026-07-13T00:00:00Z","research")
    assert AuthorityMatrix().evaluate(req).status == DecisionStatus.REJECT

def test_hidden_service_purpose_limited():
    actor=Actor("hidden",ActorType.HIDDEN_EVALUATION_SERVICE,"validation",())
    bad=AuthorityRequest("p",actor,Authority.HIDDEN_EVALUATION_ROW_ACCESS,"2026-07-13T00:00:00Z","debug")
    good=AuthorityRequest("p",actor,Authority.HIDDEN_EVALUATION_ROW_ACCESS,"2026-07-13T00:00:00Z","hidden_evaluation scoring")
    assert AuthorityMatrix().evaluate(bad).status == DecisionStatus.REJECT
    assert AuthorityMatrix().evaluate(good).status == DecisionStatus.ALLOW

def test_unknown_actor_grant_denied():
    actor=Actor("r",ActorType.HUMAN_REVIEWER,"validation",())
    req=AuthorityRequest("p",actor,Authority.SANDBOX_COMPUTE,"2026-07-13T00:00:00Z","test")
    assert AuthorityMatrix().evaluate(req).status == DecisionStatus.REJECT
