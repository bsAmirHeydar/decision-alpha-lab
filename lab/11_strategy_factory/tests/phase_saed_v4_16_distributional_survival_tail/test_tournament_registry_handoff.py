def test_baseline_preserved(load):
 t=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_TOURNAMENT.JSON');assert t['baseline_preserved'] and t['baseline_candidate_id']=='v416_empirical_km_s31' and t['promotion_decision']=='not_in_scope'
def test_registry_immutable(load):
 r=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_CHECKPOINT_REGISTRY.JSON');assert r['immutable'] and r['entry_count']==5 and not r['runtime_authority'] and not r['production_authority']
def test_handoff_gates(load):
 h=load('lab/11_strategy_factory/artifacts/saed_v4_16/V4_16_TO_V4_17_HANDOFF.JSON');assert h['next_phase']=='SAED_V4_17' and all(h['entry_gates'].values())
def test_handoff_authority_narrow(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_16/V4_16_TO_V4_17_HANDOFF.JSON')['authority'];assert a['read_frozen_distributional_survival_tail_evidence'] and a['build_reference_causal_mechanism_discovery'] and not any(a[k] for k in ['mutate_v4_16_evidence','assert_causality','rank_treatments','select_treatment','allocate_risk','sign_promotion','activate_runtime','send_order'])
def test_replay_deterministic(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_REPLAY_RECEIPT.JSON')['deterministic']
