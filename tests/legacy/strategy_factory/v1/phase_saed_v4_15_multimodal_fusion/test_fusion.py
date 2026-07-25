import pytest
@pytest.mark.parametrize('algo',['late_mean_baseline','quality_gated','masked_cross_attention_reference','evidential_product_of_experts','disagreement_aware_mixture'])
def test_algorithm_present(load,algo):
 o=load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_FUSION_OUTPUTS.JSON')['items'];x=next(v for v in o if v['algorithm']==algo);assert x['status']=='supported' and len(x['fused_embedding'])==16 and abs(sum(w['weight'] for w in x['view_weights'])-1)<1e-12
def test_baseline_present(load):
 t=load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_TOURNAMENT.JSON');assert t['baseline_preserved'] and t['baseline_candidate_id']=='v415_late_mean_s11'
def test_outputs_non_authoritative(load):
 for x in load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_FUSION_OUTPUTS.JSON')['items']:assert not x['production_eligible']
def test_gate_concentration_bounded_or_fallback(load):
 for x in load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_FUSION_OUTPUTS.JSON')['items']:
  assert x['gate_concentration']<=1
  if x['view_collapse']:assert x['directive']=='baseline'
