from __future__ import annotations
from .contracts import UpstreamIntakeContract
from .errors import UpstreamError
from .canonical import content_hash
from .authority import assert_no_authority

def validate_upstream(intake,docs):
    c=UpstreamIntakeContract.from_mapping(intake)
    pairs=[('robust_certificate','certificate_hash',c.robust_certificate_hash),('scenario_set','scenario_set_hash',c.scenario_set_hash),('ambiguity_set','ambiguity_set_hash',c.ambiguity_set_hash),('budget','ledger_hash',c.budget_ledger_hash),('handoff','handoff_hash',c.handoff_hash)]
    for doc,key,expected in pairs:
        if docs[doc].get(key)!=expected: raise UpstreamError(f'{doc} hash mismatch')
    h=docs['handoff']
    if h.get('next_phase')!='SAED_V4_22' or not h.get('research_only'): raise UpstreamError('invalid V4-21 handoff')
    assert_no_authority(h)
    required={'synthetic_generative_path_stress','bounded_path_generator_evaluation','synthetic_tail_path_coverage','stress_replay'}
    if not required<=set(h.get('allowed_next_work',[])): raise UpstreamError('handoff scope incomplete')
    out={'phase':'SAED_V4_21','hash_verified':True,'immutable':True,'research_only':True,'robust_certificate_hash':c.robust_certificate_hash,'scenario_set_hash':c.scenario_set_hash,'ambiguity_set_hash':c.ambiguity_set_hash,'budget_ledger_hash':c.budget_ledger_hash,'handoff_hash':c.handoff_hash,'intake_hash':content_hash(intake)};return out
