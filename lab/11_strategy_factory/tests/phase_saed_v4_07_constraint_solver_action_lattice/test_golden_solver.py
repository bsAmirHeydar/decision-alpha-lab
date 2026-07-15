from helpers import solve,load
def test_golden_result_exact():
 o=solve();assert o['solver_result']==load('golden_solver_result.json')
def test_golden_lattice_exact():
 o=solve();assert o['action_lattice']==load('golden_action_lattice.json')
def test_expected_counts():
 o=solve();r=o['solver_result'];l=o['action_lattice'];assert (r['candidate_count'],r['feasible_count'],r['pruned_count'])==(74,38,36);assert (l['node_count'],l['edge_count'])==(38,121)
