---
title: Path-Dependent Trailing Truth Engine
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Generate exact path-dependent labels and state transitions for tight-convex and wide-trend trailing styles.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Ordered executable price events.
- Trail state machine.
- Treatment parameters.

## Output contracts

- Trail event trace.
- Captured return, giveback, premature-exit, and re-entry labels.

## Algorithmic design

- Represent activation, ratchet, freeze, break-even, structural move, volatility move, and exit as deterministic events.
- Use tick or declared lower-timeframe path; otherwise produce lower/upper outcome bounds.
- Calculate counterfactual terminal destination after trail exit for capture/giveback diagnostics.
- Model re-entry as a separate treatment, never retroactively merge it.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No lookahead in trail updates.
- Same timestamp ordering rule frozen.
- Path resolution is part of evidence class.

## Measurement system

- Tail capture ratio.
- Giveback ratio.
- Premature exit rate.
- Path ambiguity.
- Trail parameter stability.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Trail moved using bar high before low ordering known.
- Best trail chosen on final data.
- Re-entry hides premature exits.

## UCEE integration

- None declared.

## Required tests and evidence

- Adversarial high-low order.
- Gap through trail.
- Volatility spike.
- One-tick perturbation.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Counterfactual_Outcome_Cube_V3]]
- [[Sequence_And_Path_Representation_Store]]
