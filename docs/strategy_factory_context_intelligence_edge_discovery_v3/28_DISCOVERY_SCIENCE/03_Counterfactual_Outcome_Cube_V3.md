---
title: Counterfactual Outcome Cube V3
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Evaluate every valid treatment sibling for each Context occurrence over executable market paths, including non-fill, censoring, costs, trail state, and capacity.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Occurrence cluster.
- Treatment lattice.
- Bitemporal market path.
- Broker/economics profile.

## Output contracts

- Occurrence × treatment outcome cube.
- Path/event ledger.
- Censoring and ambiguity masks.

## Algorithmic design

- Replay bid/ask and executable order state, not mid-price shortcuts.
- Store trigger, fill, partial fill, stop, target, trail, expiry, invalidation, cancel, reject, and terminal outcomes.
- Resolve same-bar ambiguity using lower-timeframe/tick data or conservative bounds.
- Preserve non-filled candidates and opportunity cost.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Replay code version and market-data role hash-bound.
- Outcome generation independent from model selection.
- Ambiguous paths cannot be optimistically resolved.

## Measurement system

- Cube coverage.
- Ambiguous-path rate.
- Fill-model error.
- Cost decomposition.
- Outcome reproducibility.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Only executed trades stored.
- Limit non-fill discarded.
- Trail evaluated from terminal OHLC.
- Future symbol specs used.

## UCEE integration

- None declared.

## Required tests and evidence

- Tick-versus-bar differential.
- Spread/slippage shock.
- Same-bar stop/target mutation.
- Partial-fill and restart.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Counterfactual_Outcome_Cube_Engine]]
- [[Path_Dependent_Trailing_Truth_Engine]]
