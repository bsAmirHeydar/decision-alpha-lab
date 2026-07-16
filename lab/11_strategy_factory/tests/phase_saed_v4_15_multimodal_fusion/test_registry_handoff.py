def test_registry_immutable(load):
 r=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_CHECKPOINT_REGISTRY.JSON');assert r['immutable'] and not r['runtime_authority'] and not r['production_authority'] and r['entry_count']==5
def test_handoff_gates(load):
 h=load('lab/11_strategy_factory/artifacts/saed_v4_15/V4_15_TO_V4_16_HANDOFF.JSON');assert h['next_phase']=='SAED_V4_16' and all(h['entry_gates'].values())
def test_handoff_no_authority_widening(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_15/V4_15_TO_V4_16_HANDOFF.JSON')['authority'];assert a['read_frozen_fusion_features'] and a['build_reference_distributional_survival_tail_models'] and not any(a[k] for k in ['mutate_v4_15_evidence','predict_outcomes','rank_treatments','select_treatment','allocate_risk','activate_runtime','send_order'])
def test_replay_deterministic(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_REPLAY_RECEIPT.JSON')['deterministic']
