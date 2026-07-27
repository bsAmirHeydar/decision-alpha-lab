from .helpers import solve
def test_pruning_is_complete():
 r=solve()['solver_result'];assert len(r['pruning_ledger']['records'])==36;assert all(x['failed_constraints'] for x in r['pruning_ledger']['records'])
def test_only_frozen_constraints_prune():
 r=solve()['solver_result'];names={n for x in r['pruning_ledger']['records'] for n in x['failed_constraints']};assert names=={'break_even_guard','target_not_below_payoff_floor'}
def test_deferred_feature_predicate_preserved():
 r=solve()['solver_result'];ordinary=[c for c in r['feasible_candidates'] if c['action_class']=='ordinary'];assert ordinary;assert all(any(e['status']=='deferred_known_time' for e in c['constraint_evaluations']) for c in ordinary)
