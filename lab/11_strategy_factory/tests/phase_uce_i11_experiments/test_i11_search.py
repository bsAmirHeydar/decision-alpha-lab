from dataclasses import replace

from strategy_factory_experiments_v3.contracts import SearchObservation
from strategy_factory_experiments_v3.enums import SearchKind
from strategy_factory_experiments_v3.golden import golden_search_plan
from strategy_factory_experiments_v3.search import (
    evolutionary_search,
    grid_search,
    hyperband_brackets,
    pareto_front,
    quasi_random_search,
    random_search,
    successive_halving_assignments,
    tpe_search,
)


def observations():
    return tuple(
        SearchObservation(
            trial_id=f"trial_{index}",
            parameter_values={"alpha": 0.001 * (index + 1), "depth": 1 + index % 4, "use_bias": bool(index % 2), "loss": "logloss" if index % 2 else "brier"},
            metrics={"validation_loss": 0.6 - index * 0.03, "latency_ms": 5.0 + index},
            feasible=True,
            resource_level=9,
            completed_sequence=index,
        )
        for index in range(8)
    )


def test_grid_search_is_exact_and_capped():
    plan = replace(golden_search_plan(SearchKind.GRID, 10), max_trials=10)
    first = grid_search(plan)
    second = grid_search(plan)
    assert first == second
    assert len(first) == 10
    assert len({item.candidate_hash for item in first}) == 10


def test_random_search_repeats_for_same_seed_and_changes_for_new_seed():
    plan = golden_search_plan(SearchKind.RANDOM, 8)
    assert random_search(plan) == random_search(plan)
    assert random_search(plan) != random_search(replace(plan, seed=18))


def test_quasi_random_search_is_unique_and_seeded():
    plan = golden_search_plan(SearchKind.QUASI_RANDOM, 12)
    proposals = quasi_random_search(plan)
    assert len(proposals) == len({item.candidate_hash for item in proposals}) == 12
    assert proposals != quasi_random_search(replace(plan, seed=plan.seed + 1))


def test_tpe_uses_quasi_random_warmup_then_deterministic_density_proposals():
    plan = golden_search_plan(SearchKind.TPE, 5)
    warmup = tpe_search(plan, observations()[:2])
    assert len(warmup) == 5
    first = tpe_search(plan, observations())
    second = tpe_search(plan, observations())
    assert first == second
    assert all(item.search_kind is SearchKind.TPE for item in first)


def test_successive_halving_keeps_best_scores_deterministically():
    trial_ids = tuple(f"t{i}" for i in range(9))
    scores = {trial_id: float(index) for index, trial_id in enumerate(trial_ids)}
    rungs = successive_halving_assignments(trial_ids, scores, min_resource=1, max_resource=9, eta=3)
    assert [r.resource_level for r in rungs] == [1, 3, 9]
    assert rungs[-1].trial_ids == ("t0",)


def test_hyperband_brackets_are_stable_and_cover_high_to_low_brackets():
    brackets = hyperband_brackets(golden_search_plan(SearchKind.HYPERBAND, 9))
    assert brackets == ((2, 9, 1), (1, 5, 3), (0, 3, 9))


def test_evolutionary_search_is_seeded_and_avoids_observed_points():
    plan = golden_search_plan(SearchKind.EVOLUTIONARY, 6)
    proposals = evolutionary_search(plan, observations())
    observed_hashes = {tuple(sorted(item.parameter_values.items())) for item in observations()}
    assert proposals == evolutionary_search(plan, observations())
    assert all(tuple(sorted(item.parameter_values.items())) not in observed_hashes for item in proposals)


def test_pareto_front_removes_dominated_observations():
    plan = golden_search_plan(SearchKind.MULTI_OBJECTIVE, 3)
    obs = (
        SearchObservation("a", {}, {"validation_loss": 0.2, "latency_ms": 10.0}, True, 1, 0),
        SearchObservation("b", {}, {"validation_loss": 0.3, "latency_ms": 12.0}, True, 1, 1),
        SearchObservation("c", {}, {"validation_loss": 0.1, "latency_ms": 20.0}, True, 1, 2),
    )
    assert [item.trial_id for item in pareto_front(obs, plan.objectives)] == ["a", "c"]
