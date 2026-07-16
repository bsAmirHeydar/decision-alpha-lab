def test_attribution_not_causal(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_ATTRIBUTION_REPORT.JSON');assert a['attention_or_gate_weights_are_not_causal'] and all(not x['causal_interpretation_permitted'] for x in a['rows'])
def test_ablation_all_views(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_ABLATION_REPORT.JSON');assert a['row_count']==16 and a['diagnostic_only']
def test_permutation_invariance(load):
 p=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_PERMUTATION_REPORTS.JSON');assert all(x['permutation_invariant'] for x in p['items'])
def test_disagreement_rows(load):
 d=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_DISAGREEMENT_REPORT.JSON');assert d['row_count']==5 and not d['attention_is_causal']
