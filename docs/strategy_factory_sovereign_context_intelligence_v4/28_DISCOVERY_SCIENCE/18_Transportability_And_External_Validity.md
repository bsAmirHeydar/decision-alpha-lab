---
title: Transportability and External Validity
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Test whether a Context setup survives changes in symbol, feed, broker, session, volatility, geography, and market regime.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Source evidence.
- Target-domain data and support map.
- Transport assumptions.

## Output contracts

- Transport matrix.
- Target-specific calibration or rejection.

## Algorithmic design

- Leave-domain-out validation.
- Density-ratio and covariate-shift diagnostics.
- Causal transport diagrams where defensible.
- Re-run execution economics per target.
- Require local calibration and capacity evidence.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No universal claim from one domain.
- Unsupported targets rejected.
- Transport tuning counts as new search.

## Measurement system

- Transport utility.
- Calibration shift.
- Support overlap.
- Execution degradation.
- Negative-transfer rate.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Same symbol name across brokers treated identical.
- US session edge claimed global.
- Feed corrections ignored.

## UCEE integration

- None declared.

## Required tests and evidence

- Broker/feed swap.
- Session holdout.
- Symbol-family holdout.
- Regime holdout.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Broker_And_Feed_Transport_Lab]]
- [[Context_Transfer_And_Negative_Transfer_Control]]
