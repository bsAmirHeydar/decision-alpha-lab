from saed_v4_robust_optimization_regret.scenarios import compile_scenarios
from saed_v4_robust_optimization_regret.allocations import enumerate_allocations
from saed_v4_robust_optimization_regret.regret import regret_matrix,dynamic_regret

def build(config,score):
 s=compile_scenarios(score,config['scenario'],config['ambiguity']);c={r['treatment_id']:r['complexity'] for r in score['rows']};a=enumerate_allocations(s['treatments'],config['optimization'],c);return s,a
def test_pure_allocations_present(config,score):
 s,a=build(config,score)
 for t in s['treatments']:assert any(x['allocation_id']==f'allocation::{t}:1.000000' for x in a['allocations'])
def test_weights_sum_one(config,score):
 _,a=build(config,score)
 for x in a['allocations']:assert abs(sum(x['weights'].values())-1)<1e-12 and x['active_count']<=config['optimization']['max_active_treatments']
def test_regret_nonnegative(config,score):
 s,a=build(config,score);r=regret_matrix(a['allocations'],s,config['optimization']['complexity_penalty'])
 assert all(v>=-1e-12 for row in r['rows'] for v in row['scenario_regret'].values())
def test_dynamic_regret():
 r=dynamic_regret([1,2,1],[2,2,3]);assert r['cumulative_regret']==3 and r['step_count']==3
