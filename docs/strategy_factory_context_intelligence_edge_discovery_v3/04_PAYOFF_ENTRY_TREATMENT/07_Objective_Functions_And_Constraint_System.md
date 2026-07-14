---
title: Objective Functions and Constraint System
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Optimize profile-specific goals while comparing all candidates through a common constrained economic utility.

## Capability tier

**Core Production**

## System design

### Lexicographic constraints

Hard validity, cost, reward floor, tail risk, capacity, support, and risk constraints are evaluated before optimization.

### Profile objectives

Hit rate, convex utility, tail capture, trend capture, or precision are optimized only inside their profile.

### Common utility

Net expected utility incorporates opportunity probability, fill, return distribution, drawdown contribution, capital occupancy, costs, and uncertainty penalty.

### Lower-confidence selection

Selection uses conservative lower bounds or robust objectives rather than point estimates alone.

## Input contracts

- `ObjectiveProfile`
- `ConstraintSet`
- `OutcomeDistribution`
- `UncertaintyBundle`

## Output contracts

- `CandidateUtility`
- `ConstraintViolations`
- `ParetoFront`

## Measurement framework

- Expected utility and lower confidence bound.
- CVaR/expected shortfall.
- Capital-time efficiency.
- Coverage-adjusted utility.

## Adversarial questions

- Can one profile win by violating another profile's hard constraints?
- Does a weighted sum hide catastrophic tradeoffs?
- Are uncertainty penalties calibrated?

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

- [[Distributionally_Robust_Utility]]
- [[Conformal_Risk_Control]]
