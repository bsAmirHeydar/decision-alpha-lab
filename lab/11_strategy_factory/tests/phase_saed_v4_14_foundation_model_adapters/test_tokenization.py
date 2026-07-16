from saed_v4_foundation_model_adapters.validation import validate_config
from saed_v4_foundation_model_adapters.tokenization import compile_token_sequence

def test_known_time_sequence(inputs):
 c=validate_config(inputs['adapter_config_doc']);s=compile_token_sequence(inputs['v413_graph'],inputs['v413_embeddings'],inputs['v413_handoff']['reference_champion_id'],c);assert s['sequence_length']<=c.sequence_length and all(t['known_time']<=s['known_as_of'] for t in s['tokens'])
def test_deterministic_tokens(inputs):
 c=validate_config(inputs['adapter_config_doc']);a=compile_token_sequence(inputs['v413_graph'],inputs['v413_embeddings'],inputs['v413_handoff']['reference_champion_id'],c);b=compile_token_sequence(inputs['v413_graph'],inputs['v413_embeddings'],inputs['v413_handoff']['reference_champion_id'],c);assert a==b
def test_causal_normalization_finite(inputs):
 c=validate_config(inputs['adapter_config_doc']);s=compile_token_sequence(inputs['v413_graph'],inputs['v413_embeddings'],inputs['v413_handoff']['reference_champion_id'],c);assert all(abs(x)<1e9 for t in s['tokens'] for x in t['feature'])
