from saed_v4_foundation_model_adapters.validation import *
from saed_v4_foundation_model_adapters.perturbation import future_suffix_audit,fail_closed_audit

def test_future_suffix_invariance(inputs):
 c=validate_config(inputs['adapter_config_doc']);ins=validate_intakes(inputs['intake_docs']);cs=validate_candidates(inputs['candidate_docs'],ins)
 for cand in cs:assert future_suffix_audit(inputs['v413_graph'],inputs['v413_embeddings'],inputs['v413_handoff']['reference_champion_id'],c,cand)['passed']
def test_fail_closed_to_baseline(inputs,bundle):
 ins=validate_intakes(inputs['intake_docs']);cs=validate_candidates(inputs['candidate_docs'],ins);cand=next(x for x in cs if x.family!='native_linear_baseline');dec={'decision':'quarantine'};dom={'supported':False};a=fail_closed_audit(cand,dec,dom);assert a['passed'] and a['resolved_path']=='native_linear_baseline'
def test_baseline_fail_closed_to_abstain(inputs):
 ins=validate_intakes(inputs['intake_docs']);cand=next(x for x in validate_candidates(inputs['candidate_docs'],ins) if x.family=='native_linear_baseline');a=fail_closed_audit(cand,{'decision':'quarantine'},{'supported':False});assert a['resolved_path']=='abstain'
