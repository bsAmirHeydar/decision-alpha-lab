def test_backdoor_not_claimed(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_BACKDOOR_AUDIT.JSON');assert not x['identification_claim_allowed']
def test_frontdoor_not_claimed(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_FRONTDOOR_AUDIT.JSON');assert not x['frontdoor_identification_claim_allowed']
def test_orthogonal_score_not_causal(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_ORTHOGONAL_SCORE_REPORT.JSON');assert not x['causal_effect_claim_allowed'] and not x['production_eligible']
def test_claim_ceiling_enforced(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_CLAIM_TIER_REPORT.JSON');assert not x['real_causal_claim'] and x['claim_ceiling']=='mechanism_compatible_synthetic_not_causal'
def test_ground_truth_synthetic_only(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_SYNTHETIC_GROUND_TRUTH_GRAPH.JSON');assert x['synthetic_benchmark_truth_only'] and not x['claimable_as_real_mechanism']
