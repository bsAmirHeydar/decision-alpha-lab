import pytest,math

@pytest.mark.parametrize('index',range(4))
def test_ate_finite(load,art,index):
 x=load(f'{art}/GOLDEN_ATE_REPORT.JSON')['effects'][index];assert all(math.isfinite(x[k]) for k in ['estimate','standard_error','lower_95','upper_95'])

def test_baseline_ate_zero(load,art):
 x=load(f'{art}/GOLDEN_ATE_REPORT.JSON');b=next(v for v in x['effects'] if v['treatment_id']==x['baseline_treatment_id']);assert abs(b['estimate'])<1e-12

@pytest.mark.parametrize('treatment', ['t_manual','t_adaptive_a','t_adaptive_b'])
def test_cate_models_present(load,art,treatment):assert treatment in load(f'{art}/GOLDEN_CATE_REPORT.JSON')['models']

def test_subgroups_complete(load,art):assert load(f'{art}/GOLDEN_SUBGROUP_REPORT.JSON')['subgroup_count']==12

def test_policy_catalog_nonruntime(load,art):
 x=load(f'{art}/GOLDEN_POLICY_CATALOG.JSON');assert x['policy_count']==7 and not x['runtime_selectable']

@pytest.mark.parametrize('policy', ['policy_skip_all','policy_fixed_manual','policy_fixed_a','policy_fixed_b','policy_manual_rule','policy_uplift_argmax','policy_conservative_lcb'])
def test_policy_values_present(load,art,policy):
 x=load(f'{art}/GOLDEN_POLICY_VALUE_REPORT.JSON');r=next(v for v in x['policies'] if v['policy_id']==policy);assert math.isfinite(r['dr_value']) and r['row_count']>0

def test_policy_value_has_no_authority(load,art):assert not load(f'{art}/GOLDEN_POLICY_VALUE_REPORT.JSON')['policy_authority']

def test_negative_control_passes(load,art):assert load(f'{art}/GOLDEN_NEGATIVE_CONTROL_REPORT.JSON')['passed']

def test_treatment_ranking_research_only(load,art):assert all(x['research_only'] for x in load(f'{art}/GOLDEN_TREATMENT_RANKING.JSON')['ranking'])
