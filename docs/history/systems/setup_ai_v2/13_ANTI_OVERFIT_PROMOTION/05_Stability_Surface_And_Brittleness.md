---
title: Stability Surface and Brittleness
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Require broad neighborhoods of acceptable performance across parameters, time, costs, and implementation choices.

## Capability tier

**Core Production**

## System design

### Parameter surfaces

Evaluate local neighborhoods, not only optimized points.

### Temporal surfaces

Rolling and expanding windows reveal regime concentration and decay.

### Economic surfaces

Spread, slippage, delay, fill, capacity, and impact perturbations.

### Implementation surfaces

Feed, bar construction, path resolution, numeric precision, and broker normalization.

## Input contracts

- `SelectedCandidate`
- `NeighborhoodPlan`
- `ScenarioLattice`

## Output contracts

- `StabilitySurface`
- `BrittlenessScore`
- `FailureDomains`

## Measurement framework

- Neighborhood retention.
- Rank stability.
- Cliff frequency.
- Worst-neighbor utility.

## Adversarial questions

- Is the optimum a needle?
- Does a one-tick change reverse results?
- Are stable averages hiding one catastrophic domain?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[Profile_Specific_Adversarial_Tests]]
