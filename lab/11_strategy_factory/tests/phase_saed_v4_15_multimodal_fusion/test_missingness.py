def test_domain_exhaustive(load):
 m=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_DOMAIN_SUBSET_MATRIX.JSON');assert m['subset_count']==1024==m['expected_subset_count'] and m['all_subsets_bounded']
def test_foundation_exhaustive(load):
 m=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_FOUNDATION_SUBSET_MATRIX.JSON');assert m['subset_count']==64==m['expected_subset_count'] and m['all_subsets_bounded']
def test_only_required_complete_domain_subsets_supported(load):
 m=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_DOMAIN_SUBSET_MATRIX.JSON');assert sum(x['supported'] for x in m['rows'])==8

def test_empty_domain_abstains(load):
 m=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_DOMAIN_SUBSET_MATRIX.JSON');x=next(r for r in m['rows'] if r['present_count']==0);assert x['directive']=='abstain'
def test_empty_foundation_baseline_only(load):
 m=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_FOUNDATION_SUBSET_MATRIX.JSON');x=next(r for r in m['rows'] if r['present_count']==0);assert x['directive']=='baseline_only'
def test_dropout_has_structured_patterns(load):
 p=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_VIEW_DROPOUT_PLAN.JSON');names={x['name'] for x in p['patterns']};assert {'complete','drop_all_optional','drop_all_foundation','drop_execution_and_liquidity','drop_time_stack'}<=names
