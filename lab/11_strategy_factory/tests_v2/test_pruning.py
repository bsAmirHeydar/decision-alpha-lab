from strategy_factory.optimization import pareto_prune, stable_budget_prune


def test_stable_budget_prune():
    assert stable_budget_prune([3,1,2], budget=2, priority=lambda x:(x,)) == (1,2)


def test_pareto_prune():
    items = [(1,1),(2,0),(0,2),(0,0)]
    result = pareto_prune(items, objectives=[lambda x:x[0], lambda x:x[1]])
    assert (0,0) not in result
    assert set(result) == {(1,1),(2,0),(0,2)}
