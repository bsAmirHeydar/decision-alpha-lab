"""Generic causality and deterministic-replay audits for view builders."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence

from .canonical import canonical_sha256, stable_id


@dataclass(frozen=True, slots=True)
class FuturePerturbationAudit:
    audit_id: str
    baseline_hash: str
    perturbed_hash: str
    passed: bool
    perturbation_count: int
    evidence_hash: str


@dataclass(frozen=True, slots=True)
class DeterministicReplayAudit:
    audit_id: str
    run_hashes: tuple[str, ...]
    passed: bool
    evidence_hash: str


def future_perturbation_audit(
    builder: Callable[[Sequence[Any]], Any],
    known_prefix: Sequence[Any],
    future_suffix: Sequence[Any],
) -> FuturePerturbationAudit:
    baseline = builder(tuple(known_prefix))
    perturbed = builder(tuple(known_prefix) + tuple(future_suffix))
    baseline_hash = canonical_sha256(baseline)
    perturbed_hash = canonical_sha256(perturbed)
    material = {
        "baseline_hash": baseline_hash,
        "perturbed_hash": perturbed_hash,
        "perturbation_count": len(future_suffix),
    }
    return FuturePerturbationAudit(
        stable_id("ucefutureaudit", material),
        baseline_hash,
        perturbed_hash,
        baseline_hash == perturbed_hash,
        len(future_suffix),
        canonical_sha256(material),
    )


def deterministic_replay_audit(factory: Callable[[], Any], runs: int = 3) -> DeterministicReplayAudit:
    if runs < 2:
        raise ValueError("deterministic replay requires at least two runs")
    hashes = tuple(canonical_sha256(factory()) for _ in range(runs))
    material = {"run_hashes": hashes, "runs": runs}
    return DeterministicReplayAudit(
        stable_id("ucereplayaudit", material),
        hashes,
        len(set(hashes)) == 1,
        canonical_sha256(material),
    )
