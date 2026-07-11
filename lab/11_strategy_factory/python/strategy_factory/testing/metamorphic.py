"""Reusable metamorphic assertions for strategy plugins and decision plans."""
from __future__ import annotations

from dataclasses import replace
from typing import Callable, Mapping, Sequence

from ..contracts import AnatomyEvent, TradeCandidate


def assert_price_translation_invariance(
    build: Callable[[AnatomyEvent, Mapping[str, float]], Sequence[TradeCandidate]],
    event: AnatomyEvent,
    context: Mapping[str, float],
    shift: float,
) -> None:
    original = tuple(build(event, context))
    shifted_event = replace(
        event,
        reference_price=event.reference_price + shift,
        invalidation_price=(
            None if event.invalidation_price is None else event.invalidation_price + shift
        ),
        event_id=event.event_id + "_shifted",
    )
    shifted_context = {
        key: (value + shift if key.endswith("_price") or key.endswith("_level") else value)
        for key, value in context.items()
    }
    shifted = tuple(build(shifted_event, shifted_context))
    if len(original) != len(shifted):
        raise AssertionError("translation changed candidate count")
    for left, right in zip(original, shifted):
        if abs((right.entry_price - left.entry_price) - shift) > 1e-9:
            raise AssertionError("entry price is not translation invariant")
        if abs((right.stop_price - left.stop_price) - shift) > 1e-9:
            raise AssertionError("stop price is not translation invariant")
        if left.target_price is not None and right.target_price is not None:
            if abs((right.target_price - left.target_price) - shift) > 1e-9:
                raise AssertionError("target price is not translation invariant")


def assert_deterministic(call: Callable[[], object], repetitions: int = 5) -> None:
    results = [call() for _ in range(repetitions)]
    first = results[0]
    if any(item != first for item in results[1:]):
        raise AssertionError("operation is not deterministic")
