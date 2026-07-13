"""Deterministic search adapters for UCE-I11.

The module provides native reference implementations for the scheduling layer.
They are intentionally modest algorithms, but their identity, seed behavior,
constraints, and accounting are exact.  Optional external optimizers may be
plugged in only if they emit the same SearchObservation and parameter identity
contracts.
"""

from __future__ import annotations

import itertools
import math
import random
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Iterable, Mapping, Sequence

from .canonical import canonical_sha256
from .contracts import ObjectiveSpec, ParameterSpec, SearchObservation, SearchPlan
from .enums import ObjectiveDirection, ParameterKind, SearchKind
from .errors import ExperimentError

_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53)


@dataclass(frozen=True, slots=True)
class SearchCandidate:
    ordinal: int
    parameter_values: Mapping[str, Any]
    resource_level: int
    search_kind: SearchKind
    candidate_hash: str


@dataclass(frozen=True, slots=True)
class RungAssignment:
    rung: int
    resource_level: int
    trial_ids: tuple[str, ...]


def _numeric_grid(spec: ParameterSpec) -> tuple[int | float, ...]:
    assert spec.low is not None and spec.high is not None
    if spec.step is None:
        return (int(spec.low), int(spec.high)) if spec.kind is ParameterKind.INTEGER else (float(spec.low), float(spec.high))
    low = Decimal(str(spec.low))
    high = Decimal(str(spec.high))
    step = Decimal(str(spec.step))
    values: list[int | float] = []
    current = low
    guard = 0
    while current <= high:
        values.append(int(current) if spec.kind is ParameterKind.INTEGER else float(current))
        current += step
        guard += 1
        if guard > 1_000_000:
            raise ExperimentError("parameter_grid_explosion", "numeric parameter grid exceeds safety guard")
    return tuple(values)


def parameter_grid(spec: ParameterSpec) -> tuple[Any, ...]:
    if spec.kind in (ParameterKind.CATEGORICAL, ParameterKind.BOOLEAN):
        return tuple(spec.values)
    return _numeric_grid(spec)


def _candidate(ordinal: int, values: Mapping[str, Any], resource: int, kind: SearchKind) -> SearchCandidate:
    payload = {
        "ordinal": ordinal,
        "parameter_values": dict(values),
        "resource_level": resource,
        "search_kind": kind.value,
    }
    return SearchCandidate(ordinal, dict(values), resource, kind, canonical_sha256(payload))


def grid_search(plan: SearchPlan) -> tuple[SearchCandidate, ...]:
    names = [parameter.name for parameter in plan.parameters]
    domains = [parameter_grid(parameter) for parameter in plan.parameters]
    if not domains:
        return (_candidate(0, dict(plan.baseline_parameters), plan.max_resource, SearchKind.GRID),)
    candidates = []
    for ordinal, combination in enumerate(itertools.product(*domains)):
        values = dict(zip(names, combination))
        candidates.append(_candidate(ordinal, values, plan.max_resource, SearchKind.GRID))
        if len(candidates) >= plan.max_trials:
            break
    return tuple(candidates)


def _quantize_numeric(spec: ParameterSpec, value: float) -> int | float:
    assert spec.low is not None and spec.high is not None
    value = min(float(spec.high), max(float(spec.low), value))
    if spec.step is not None:
        steps = round((value - float(spec.low)) / float(spec.step))
        value = float(spec.low) + steps * float(spec.step)
        value = min(float(spec.high), max(float(spec.low), value))
    if spec.kind is ParameterKind.INTEGER:
        return int(round(value))
    return float(format(value, ".15g"))


def _sample_parameter(spec: ParameterSpec, unit: float) -> Any:
    unit = min(1.0 - 1e-15, max(0.0, unit))
    if spec.kind in (ParameterKind.CATEGORICAL, ParameterKind.BOOLEAN):
        index = min(len(spec.values) - 1, int(unit * len(spec.values)))
        return spec.values[index]
    assert spec.low is not None and spec.high is not None
    if spec.log_scale:
        low_log = math.log(float(spec.low))
        high_log = math.log(float(spec.high))
        raw = math.exp(low_log + unit * (high_log - low_log))
    else:
        raw = float(spec.low) + unit * (float(spec.high) - float(spec.low))
    return _quantize_numeric(spec, raw)


def random_search(plan: SearchPlan) -> tuple[SearchCandidate, ...]:
    rng = random.Random(plan.seed)
    unique: dict[str, SearchCandidate] = {}
    attempts = 0
    max_attempts = max(plan.max_trials * 100, 100)
    while len(unique) < plan.max_trials and attempts < max_attempts:
        values = {parameter.name: _sample_parameter(parameter, rng.random()) for parameter in plan.parameters}
        digest = canonical_sha256(values)
        if digest not in unique:
            unique[digest] = _candidate(len(unique), values, plan.max_resource, SearchKind.RANDOM)
        attempts += 1
    if not unique:
        unique[canonical_sha256({})] = _candidate(0, {}, plan.max_resource, SearchKind.RANDOM)
    return tuple(unique.values())


def _halton(index: int, base: int) -> float:
    result = 0.0
    factor = 1.0 / base
    value = index
    while value > 0:
        result += factor * (value % base)
        value //= base
        factor /= base
    return result


def quasi_random_search(plan: SearchPlan) -> tuple[SearchCandidate, ...]:
    if len(plan.parameters) > len(_PRIMES):
        raise ExperimentError("quasi_random_dimension_exceeded", "native Halton adapter supports at most 16 dimensions")
    candidates: list[SearchCandidate] = []
    seen: set[str] = set()
    index = plan.seed + 1
    while len(candidates) < plan.max_trials and index < plan.seed + plan.max_trials * 100 + 1:
        values = {
            parameter.name: _sample_parameter(parameter, _halton(index, _PRIMES[dimension]))
            for dimension, parameter in enumerate(plan.parameters)
        }
        digest = canonical_sha256(values)
        if digest not in seen:
            candidates.append(_candidate(len(candidates), values, plan.max_resource, SearchKind.QUASI_RANDOM))
            seen.add(digest)
        index += 1
    return tuple(candidates)


def _objective_score(metrics: Mapping[str, float], objectives: Sequence[ObjectiveSpec]) -> float:
    score = 0.0
    for objective in objectives:
        if objective.name not in metrics:
            raise ExperimentError("objective_metric_missing", "search observation is missing an objective metric", {"metric": objective.name})
        value = float(metrics[objective.name])
        if objective.constraint_min is not None and value < objective.constraint_min:
            return math.inf
        if objective.constraint_max is not None and value > objective.constraint_max:
            return math.inf
        signed = value if objective.direction is ObjectiveDirection.MINIMIZE else -value
        score += objective.weight * signed
    return score


def tpe_search(plan: SearchPlan, observations: Sequence[SearchObservation]) -> tuple[SearchCandidate, ...]:
    """Deterministic lightweight TPE-style proposal generator.

    The native reference partitions feasible observations into good/bad sets,
    samples around good numeric parameters, and chooses categories using
    Laplace-smoothed good/bad frequency ratios.  It is not a replacement for a
    full external TPE package; it is the deterministic contract floor.
    """

    feasible = [observation for observation in observations if observation.feasible]
    if len(feasible) < plan.warmup_trials:
        warmup = SearchPlan(
            plan.search_id,
            plan.search_version,
            SearchKind.QUASI_RANDOM,
            plan.parameters,
            plan.max_trials,
            plan.seed,
            plan.objectives,
            plan.baseline_parameters,
            plan.eta,
            plan.min_resource,
            plan.max_resource,
            plan.warmup_trials,
        )
        return quasi_random_search(warmup)

    ranked = sorted(feasible, key=lambda observation: (_objective_score(observation.metrics, plan.objectives), observation.trial_id))
    cut = max(1, int(math.ceil(len(ranked) * 0.2)))
    good = ranked[:cut]
    bad = ranked[cut:] or ranked[-1:]
    rng = random.Random(plan.seed + len(observations) * 104729)
    proposals: list[SearchCandidate] = []
    seen = {canonical_sha256(observation.parameter_values) for observation in observations}
    attempts = 0
    while len(proposals) < plan.max_trials and attempts < plan.max_trials * 200:
        values: dict[str, Any] = {}
        for parameter in plan.parameters:
            good_values = [observation.parameter_values[parameter.name] for observation in good]
            bad_values = [observation.parameter_values[parameter.name] for observation in bad]
            if parameter.kind in (ParameterKind.CATEGORICAL, ParameterKind.BOOLEAN):
                domain = parameter_grid(parameter)
                ratios = []
                for choice in domain:
                    good_count = 1 + sum(value == choice for value in good_values)
                    bad_count = 1 + sum(value == choice for value in bad_values)
                    ratios.append(good_count / bad_count)
                total = sum(ratios)
                cursor = rng.random() * total
                selected = domain[-1]
                for choice, ratio in zip(domain, ratios):
                    cursor -= ratio
                    if cursor <= 0:
                        selected = choice
                        break
                values[parameter.name] = selected
            else:
                anchor = float(good_values[int(rng.random() * len(good_values))])
                spread = max(1e-12, (float(parameter.high) - float(parameter.low)) / max(3.0, math.sqrt(len(good))))
                values[parameter.name] = _quantize_numeric(parameter, rng.gauss(anchor, spread))
        digest = canonical_sha256(values)
        if digest not in seen:
            proposals.append(_candidate(len(proposals), values, plan.max_resource, SearchKind.TPE))
            seen.add(digest)
        attempts += 1
    return tuple(proposals)


def successive_halving_assignments(
    trial_ids: Sequence[str],
    scores: Mapping[str, float],
    *,
    min_resource: int,
    max_resource: int,
    eta: int,
) -> tuple[RungAssignment, ...]:
    if eta < 2 or min_resource < 1 or max_resource < min_resource:
        raise ExperimentError("invalid_halving_configuration", "successive halving configuration is invalid")
    current = tuple(sorted(trial_ids))
    if not current:
        return ()
    rungs: list[RungAssignment] = []
    resource = min_resource
    rung = 0
    while current:
        rungs.append(RungAssignment(rung, resource, current))
        if resource >= max_resource or len(current) == 1:
            break
        missing = [trial_id for trial_id in current if trial_id not in scores]
        if missing:
            raise ExperimentError("halving_score_missing", "scores are missing for a rung", {"missing": missing})
        keep = max(1, math.ceil(len(current) / eta))
        current = tuple(sorted(current, key=lambda trial_id: (scores[trial_id], trial_id))[:keep])
        resource = min(max_resource, resource * eta)
        rung += 1
    return tuple(rungs)


def hyperband_brackets(plan: SearchPlan) -> tuple[tuple[int, int, int], ...]:
    """Return deterministic (bracket, initial_trials, initial_resource) tuples."""
    s_max = int(math.floor(math.log(plan.max_resource / plan.min_resource, plan.eta))) if plan.max_resource > plan.min_resource else 0
    brackets: list[tuple[int, int, int]] = []
    for bracket in range(s_max, -1, -1):
        initial_trials = int(math.ceil((s_max + 1) / (bracket + 1) * (plan.eta**bracket)))
        initial_resource = max(plan.min_resource, int(plan.max_resource / (plan.eta**bracket)))
        brackets.append((bracket, initial_trials, initial_resource))
    return tuple(brackets)


def evolutionary_search(
    plan: SearchPlan,
    observations: Sequence[SearchObservation],
    *,
    elite_fraction: float = 0.25,
) -> tuple[SearchCandidate, ...]:
    if not 0 < elite_fraction <= 1:
        raise ExperimentError("invalid_elite_fraction", "elite_fraction must be in (0, 1]")
    feasible = [observation for observation in observations if observation.feasible]
    if not feasible:
        return random_search(plan)
    ranked = sorted(feasible, key=lambda observation: (_objective_score(observation.metrics, plan.objectives), observation.trial_id))
    elite_count = max(1, int(math.ceil(len(ranked) * elite_fraction)))
    elites = ranked[:elite_count]
    rng = random.Random(plan.seed + len(observations) * 65537)
    seen = {canonical_sha256(observation.parameter_values) for observation in observations}
    proposals: list[SearchCandidate] = []
    attempts = 0
    while len(proposals) < plan.max_trials and attempts < plan.max_trials * 200:
        parent_a = elites[int(rng.random() * len(elites))]
        parent_b = elites[int(rng.random() * len(elites))]
        values: dict[str, Any] = {}
        for parameter in plan.parameters:
            base = parent_a.parameter_values[parameter.name] if rng.random() < 0.5 else parent_b.parameter_values[parameter.name]
            if rng.random() < 0.25:
                if parameter.kind in (ParameterKind.CATEGORICAL, ParameterKind.BOOLEAN):
                    base = parameter.values[int(rng.random() * len(parameter.values))]
                else:
                    assert parameter.low is not None and parameter.high is not None
                    sigma = (float(parameter.high) - float(parameter.low)) * 0.1
                    base = _quantize_numeric(parameter, rng.gauss(float(base), sigma))
            values[parameter.name] = base
        digest = canonical_sha256(values)
        if digest not in seen:
            proposals.append(_candidate(len(proposals), values, plan.max_resource, SearchKind.EVOLUTIONARY))
            seen.add(digest)
        attempts += 1
    return tuple(proposals)


def is_feasible(observation: SearchObservation, objectives: Sequence[ObjectiveSpec]) -> bool:
    if not observation.feasible:
        return False
    for objective in objectives:
        value = observation.metrics.get(objective.name)
        if value is None:
            return False
        if objective.constraint_min is not None and value < objective.constraint_min:
            return False
        if objective.constraint_max is not None and value > objective.constraint_max:
            return False
    return True


def pareto_front(
    observations: Sequence[SearchObservation], objectives: Sequence[ObjectiveSpec]
) -> tuple[SearchObservation, ...]:
    feasible = [observation for observation in observations if is_feasible(observation, objectives)]

    def dominates(left: SearchObservation, right: SearchObservation) -> bool:
        no_worse = True
        strictly_better = False
        for objective in objectives:
            lv = left.metrics[objective.name]
            rv = right.metrics[objective.name]
            if objective.direction is ObjectiveDirection.MINIMIZE:
                no_worse &= lv <= rv
                strictly_better |= lv < rv
            else:
                no_worse &= lv >= rv
                strictly_better |= lv > rv
        return bool(no_worse and strictly_better)

    front = [item for item in feasible if not any(dominates(other, item) for other in feasible if other is not item)]
    return tuple(sorted(front, key=lambda item: item.trial_id))


def propose(plan: SearchPlan, observations: Sequence[SearchObservation] = ()) -> tuple[SearchCandidate, ...]:
    if plan.kind is SearchKind.BASELINE:
        return (_candidate(0, dict(plan.baseline_parameters), plan.max_resource, SearchKind.BASELINE),)
    if plan.kind is SearchKind.GRID:
        return grid_search(plan)
    if plan.kind is SearchKind.RANDOM:
        return random_search(plan)
    if plan.kind is SearchKind.QUASI_RANDOM:
        return quasi_random_search(plan)
    if plan.kind is SearchKind.TPE:
        return tpe_search(plan, observations)
    if plan.kind is SearchKind.EVOLUTIONARY:
        return evolutionary_search(plan, observations)
    if plan.kind in (SearchKind.SUCCESSIVE_HALVING, SearchKind.HYPERBAND, SearchKind.MULTI_OBJECTIVE):
        # Candidate generation is quasi-random; pruning/brackets/selection are
        # represented by dedicated deterministic functions above.
        shadow = SearchPlan(
            plan.search_id,
            plan.search_version,
            SearchKind.QUASI_RANDOM,
            plan.parameters,
            plan.max_trials,
            plan.seed,
            plan.objectives,
            plan.baseline_parameters,
            plan.eta,
            plan.min_resource,
            plan.max_resource,
            plan.warmup_trials,
        )
        return quasi_random_search(shadow)
    raise ExperimentError("unsupported_search_kind", "search kind is not registered", {"kind": plan.kind.value})
