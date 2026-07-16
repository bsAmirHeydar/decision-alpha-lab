import pytest
@pytest.mark.parametrize('name',['AUTHORITY_BOUNDARY.JSON','CLAIM_LEDGER.JSON','CONFORMANCE_RESULTS.JSON','GOLDEN_CAUSAL_BENCHMARK_DATASET.JSON','GOLDEN_TEMPORAL_CANDIDATE_GRAPH.JSON','GOLDEN_INVARIANT_MECHANISM_REPORT.JSON','GOLDEN_NEGATIVE_CONTROL_AUDIT.JSON','GOLDEN_TOURNAMENT.JSON','GOLDEN_CHECKPOINT_REGISTRY.JSON','V4_17_TO_V4_18_HANDOFF.JSON'])
def test_artifact_exists(root,name):assert (root/'lab/11_strategy_factory/artifacts/saed_v4_17'/name).is_file()
def test_integrity_receipt(load):
 x=load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_INTEGRITY_RECEIPT.JSON');assert x['deterministic'] and x['synthetic_only'] and x['protected_evidence_exposures']==0 and not x['causal_claim_authority']
def test_replay(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_REPLAY_RECEIPT.JSON')['deterministic_replay_passed']
def test_handoff_gates(load):assert all(load('lab/11_strategy_factory/artifacts/saed_v4_17/V4_17_TO_V4_18_HANDOFF.JSON')['entry_gates'].values())
def test_handoff_authority_narrow(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_17/V4_17_TO_V4_18_HANDOFF.JSON')['authority'];assert a['read_frozen_causal_mechanism_evidence'] and a['build_reference_causal_treatment_and_policy_value'] and not any(a[k] for k in ['mutate_v4_17_evidence','assert_real_causality','estimate_production_treatment_effect','rank_treatments','select_treatment','allocate_risk','sign_promotion','activate_runtime','send_order'])
