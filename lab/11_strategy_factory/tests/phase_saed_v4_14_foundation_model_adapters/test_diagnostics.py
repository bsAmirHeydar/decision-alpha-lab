from saed_v4_foundation_model_adapters.validation import *
from saed_v4_foundation_model_adapters.tokenization import compile_token_sequence
from saed_v4_foundation_model_adapters.adapters import run_adapter
from saed_v4_foundation_model_adapters.calibration import calibrate
from saed_v4_foundation_model_adapters.domain_shift import assess
from saed_v4_foundation_model_adapters.objectives import evaluate

def rows(inputs):
 c=validate_config(inputs['adapter_config_doc']);ins=validate_intakes(inputs['intake_docs']);cs=validate_candidates(inputs['candidate_docs'],ins);p=validate_domain_shift_policy(inputs['domain_policy_doc']);s=compile_token_sequence(inputs['v413_graph'],inputs['v413_embeddings'],inputs['v413_handoff']['reference_champion_id'],c)
 for x in cs:
  f=run_adapter(s,c,x);cal=calibrate(f,s,x);dom=assess(s,f,x,p);yield evaluate(s,f,cal,dom,x,c),cal,dom

def test_diagnostic_ranges(inputs):
 for e,c,d in rows(inputs):
  assert 0<=e['composite_score']<=1 and 0<=c['calibration_score']<=1 and 0<=d['robustness_score']<=1
def test_no_outcome_labels(inputs):assert all(not e['outcome_labels_used'] for e,_,_ in rows(inputs))
def test_domain_support_explicit(inputs):assert all(isinstance(d['supported'],bool) and 'unsupported_action' in d for _,_,d in rows(inputs))
