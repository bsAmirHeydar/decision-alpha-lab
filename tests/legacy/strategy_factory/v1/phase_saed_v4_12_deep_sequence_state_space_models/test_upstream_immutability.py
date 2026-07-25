import hashlib,json

def test_upstream_hashes_match_handoff(root,load):
 h=load('releases/history/strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON');pairs=[('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON','encoder_checkpoint_hash','checkpoint_hash'),('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKENIZER_SPEC.JSON','tokenizer_hash','tokenizer_hash'),('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_CHECKPOINT_REGISTRY.JSON','checkpoint_registry_hash','registry_hash')]
 for path,hk,dk in pairs:assert load(path)[dk]==h[hk]
