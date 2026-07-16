from saed_v4_foundation_model_adapters.validation import validate_config,validate_intakes,validate_candidates
from saed_v4_foundation_model_adapters.tokenization import compile_token_sequence
from saed_v4_foundation_model_adapters.adapters import run_adapter

def setup(inputs):
 c=validate_config(inputs['adapter_config_doc']);i=validate_intakes(inputs['intake_docs']);cs=validate_candidates(inputs['candidate_docs'],i);s=compile_token_sequence(inputs['v413_graph'],inputs['v413_embeddings'],inputs['v413_handoff']['reference_champion_id'],c);return c,cs,s
def test_all_adapter_families(inputs):
 c,cs,s=setup(inputs);rows=[run_adapter(s,c,x) for x in cs];assert len(rows)==6 and len({x['adapter_mode'] for x in rows})==6

def test_quantiles_monotone(inputs):
 c,cs,s=setup(inputs)
 for row in [run_adapter(s,c,x) for x in cs]:
  values=[q['value'] for q in row['quantile_forecast']];assert values==sorted(values)
def test_no_external_model_invocation(inputs):
 c,cs,s=setup(inputs);assert all(not run_adapter(s,c,x)['external_model_invoked'] for x in cs)
def test_deterministic_adapter_outputs(inputs):
 c,cs,s=setup(inputs)
 for x in cs:assert run_adapter(s,c,x)==run_adapter(s,c,x)
