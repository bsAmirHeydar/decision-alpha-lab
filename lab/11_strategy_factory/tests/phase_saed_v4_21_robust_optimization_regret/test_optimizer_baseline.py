import copy,pytest

def test_report_counts(result):
 r=result['optimization_report'];assert r['allocation_count']>=5 and r['feasible_count']>=1 and len(r['rows'])==r['allocation_count']
def test_baselines_preserved(result):
 b=result['optimization_report']['baseline_report'];assert b['manual_baseline_preserved'] and b['skip_preserved'] and b['fail_to_skip']
def test_decision_no_authority(result):
 d=result['optimization_report']['decision'];assert not d['runtime_executable'] and not d['decision_authority'] and not d['risk_allocation_authority']
def test_objective_rows_sorted(result):assert result['optimization_report']['rows'][0]['feasible']
@pytest.mark.parametrize('objective',['maximin_utility','minimax_regret','distributionally_robust','robust_cvar','lexicographic'])
def test_objective_variants(config,upstream,score,objective):
 from saed_v4_robust_optimization_regret.service import run_reference
 x=copy.deepcopy(config);x['optimization']['objective']=objective;r=run_reference(x,upstream,score);assert r['optimization_report']['objective']==objective
