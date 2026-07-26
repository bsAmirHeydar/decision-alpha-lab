---
title: Survival and Competing Risks
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Model time to fill, stop, target, trail exit, context expiry, and invalidation with censoring-aware methods.

## Capability tier

**Core Production**

## System design

### Event schema

Mutually exclusive or multi-state event definitions are frozen per treatment family.

### Censoring

Right censoring, administrative censoring, non-fill, session close, and data loss are distinguished.

### Methods

Kaplan–Meier/Aalen-Johansen baselines, Cox and flexible parametric models, survival forests, and neural survival challengers.

### Policy use

Hazards inform expiry, waiting, trail, and selection but cannot invent events outside the treatment state machine.

## Input contracts

- `EventHistoryRows`
- `CensoringPolicy`
- `TreatmentStateMachine`

## Output contracts

- `HazardCurves`
- `CumulativeIncidence`
- `SurvivalCalibration`

## Measurement framework

- Time-dependent concordance.
- Integrated Brier score.
- Cause-specific calibration.
- Horizon stability.

## Adversarial questions

- Is censoring informative and ignored?
- Are competing events merged into win/loss?
- Does future maximum define event timing?

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

- [[Fill_Hazard_And_Adverse_Selection]]
