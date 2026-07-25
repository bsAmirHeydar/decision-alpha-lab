import json,pytest
@pytest.mark.parametrize('name',['AUTHORITY_BOUNDARY.JSON','CLAIM_LEDGER.JSON','CONFORMANCE_RESULTS.JSON','GOLDEN_SURVIVAL_DATASET.JSON','GOLDEN_SURVIVAL_PREDICTIONS.JSON','GOLDEN_DISTRIBUTIONAL_PREDICTIONS.JSON','GOLDEN_TAIL_CALIBRATION_REPORT.JSON','GOLDEN_TOURNAMENT.JSON','GOLDEN_CHECKPOINT_REGISTRY.JSON','V4_16_TO_V4_17_HANDOFF.JSON'])
def test_artifact_exists(root,name):
 p=root/'releases/history/strategy_factory/artifacts/saed_v4_16'/name;assert p.is_file();json.loads(p.read_text())
def test_claims_conservative(load):
 c=load('releases/history/strategy_factory/artifacts/saed_v4_16/CLAIM_LEDGER.JSON')['claims'];assert c['distributional_survival_tail_boundary_implemented'] and c['censored_is_not_outcome'] and not c['real_outcome_prediction'] and not c['causal_claim'] and not c['production_authorization'] and not c['live_trading']
def test_conformance(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_16/CONFORMANCE_RESULTS.JSON')['passed']
