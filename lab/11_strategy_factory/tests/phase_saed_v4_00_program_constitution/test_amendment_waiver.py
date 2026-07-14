from saed_v4_constitution.amendments import AmendmentGate
from saed_v4_constitution.enums import DecisionStatus
from saed_v4_constitution.models import AmendmentProposal,ReviewApproval
from saed_v4_constitution.waivers import WaiverGate,WaiverRequest

def approvals():
 return (ReviewApproval('r1','validation','reviewer','2026-07-13T00:00:00Z','approve','ok','1'*64),ReviewApproval('r2','risk','reviewer','2026-07-13T00:00:00Z','approve','ok','2'*64))

def proposal(researcher,**kw):
 d=dict(amendment_id='a',program_id='p',proposer=researcher,current_constitution_hash='a'*64,target_section='objective',current_value_hash='b'*64,proposed_value={'x':1},rationale='improve',known_time='2026-07-13T00:00:00Z',effective_from='2026-08-01T00:00:00Z',applies_to_existing_programs=False,expires_at='2026-07-31T00:00:00Z',approvals=approvals())
 d.update(kw); return AmendmentProposal(**d)

def test_valid_amendment(researcher): assert AmendmentGate().evaluate(proposal(researcher),'a'*64).status == DecisionStatus.ALLOW

def test_amendment_lineage_mismatch(researcher): assert AmendmentGate().evaluate(proposal(researcher),'c'*64).status == DecisionStatus.REJECT

def test_retroactive_amendment_rejected(researcher): assert AmendmentGate().evaluate(proposal(researcher,applies_to_existing_programs=True),'a'*64).status == DecisionStatus.REJECT

def test_hard_authority_not_amendable(researcher): assert AmendmentGate().evaluate(proposal(researcher,target_section='authority.order'),'a'*64).status == DecisionStatus.REJECT

def test_non_waivable_rule_rejected():
 w=WaiverRequest('w','p','no_order_authority','x','2026-07-13T00:00:00Z','2026-07-14T00:00:00Z','2026-07-20T00:00:00Z','test',('control',),('a','b'))
 assert WaiverGate().evaluate(w).status == DecisionStatus.REJECT

def test_valid_time_bounded_waiver():
 w=WaiverRequest('w','p','report_format','x','2026-07-13T00:00:00Z','2026-07-14T00:00:00Z','2026-07-20T00:00:00Z','test',('manual review',),('a','b'))
 assert WaiverGate().evaluate(w).status == DecisionStatus.ALLOW

def test_waiver_requires_two_approvals():
 w=WaiverRequest('w','p','report_format','x','2026-07-13T00:00:00Z','2026-07-14T00:00:00Z','2026-07-20T00:00:00Z','test',('manual review',),('a',))
 assert WaiverGate().evaluate(w).status == DecisionStatus.REQUIRE_REVIEW
