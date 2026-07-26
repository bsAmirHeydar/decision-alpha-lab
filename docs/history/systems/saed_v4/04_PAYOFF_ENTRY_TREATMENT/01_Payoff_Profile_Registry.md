---
title: Payoff Profile Registry
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Formalize the five economic styles as different objective and risk geometries rather than forcing them onto one leaderboard.

## Capability tier

**Core Production**

## System design

### P1 Wide-Survival High-Hit Fixed

Wide structural invalidation, fixed destination with net reward not below 1R, optimized for calibrated hit rate subject to capital and tail constraints.

### P2 Tight-Convex Fixed

Tight trigger invalidation and fixed or structural destination, optimized for positive skew and right-tail expectancy rather than win rate.

### P3 Tight-Convex Trail

Tight invalidation with path-dependent trailing, optimized for robust tail capture under giveback and premature-exit constraints.

### P4 Wide-Survival Open Trail

Wide structural survival and open target, optimized for trend persistence, capture, and capital efficiency.

### P5 Tight-Precision High-Hit Fixed

Tight invalidation and modest reward at or above 1R, optimized for calibrated precision under execution stress.

## Input contracts

- `PayoffProfileVersion`
- `EconomicsContract`
- `RiskConstraints`

## Output contracts

- `ObjectiveProfile`
- `ProfileScorecard`
- `ProfileEligibility`

## Measurement framework

- Profile-specific utility.
- Cross-profile normalized economic utility.
- Capital occupancy, tail loss, and drawdown.

## Adversarial questions

- Is a high win rate purchased by hidden tail risk?
- Is convexity dependent on a few trades?
- Does trailing exploit intrabar assumptions?
- Does tight precision survive real spread and delay?

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

- [[Objective_Functions_And_Constraint_System]]
