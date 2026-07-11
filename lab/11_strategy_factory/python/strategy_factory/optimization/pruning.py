"""Candidate dominance and budget pruning."""
from __future__ import annotations

from typing import Callable, Sequence, TypeVar

T = TypeVar("T")


def stable_budget_prune(
    items: Sequence[T],
    *,
    budget: int,
    priority: Callable[[T], tuple],
) -> tuple[T, ...]:
    if budget <= 0:
        return ()
    return tuple(sorted(items, key=priority)[:budget])


def pareto_prune(
    items: Sequence[T],
    *,
    objectives: Sequence[Callable[[T], float]],
    minimize: Sequence[bool] | None = None,
) -> tuple[T, ...]:
    """Return the non-dominated subset with deterministic original ordering."""
    if not items:
        return ()
    minimize = tuple(minimize or [False] * len(objectives))
    if len(minimize) != len(objectives):
        raise ValueError("minimize flags must match objectives")
    vectors = [tuple(fn(item) for fn in objectives) for item in items]

    def dominates(a: tuple[float, ...], b: tuple[float, ...]) -> bool:
        comparable_a = tuple(-x if mn else x for x, mn in zip(a, minimize))
        comparable_b = tuple(-x if mn else x for x, mn in zip(b, minimize))
        return all(x >= y for x, y in zip(comparable_a, comparable_b)) and any(
            x > y for x, y in zip(comparable_a, comparable_b)
        )

    keep: list[T] = []
    for i, item in enumerate(items):
        if not any(i != j and dominates(vectors[j], vectors[i]) for j in range(len(items))):
            keep.append(item)
    return tuple(keep)
