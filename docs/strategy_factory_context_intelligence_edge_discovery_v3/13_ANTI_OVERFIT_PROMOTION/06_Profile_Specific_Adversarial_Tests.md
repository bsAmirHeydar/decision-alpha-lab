---
title: Profile-Specific Adversarial Tests
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Attack each payoff profile using the failure modes most likely to manufacture its apparent edge.

## Capability tier

**Core Production**

## System design

### P1

Stop widening, hidden tail loss, long holding time, target feasibility, and capital occupancy.

### P2

Best-trade removal, tail bootstrap, destination sensitivity, and losing-streak distribution.

### P3

Intrabar ordering, trail neighborhood, giveback, premature exit, and path-resolution parity.

### P4

Trend scarcity, chop loss, regime transition, time underwater, and correlated trend failure.

### P5

Tick/feed variation, spread/slippage, one-tick and one-bar delay, stop-level and exact-entry sensitivity.

## Input contracts

- `ProfileCandidate`
- `PathReplay`
- `ExecutionScenarios`

## Output contracts

- `ProfileChallengeDossier`
- `FailureMap`
- `PromotionImpact`

## Measurement framework

- Adversarial survival by profile.
- Worst-case utility.
- Risk-budget impact.
- Evidence downgrade.

## Adversarial questions

- Did the generic test suite miss the profile's unique fragility?
- Are adversarial parameters realistic?
- Are failed profile variants still reported?

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

- [[Payoff_Profile_Registry]]
