---
title: Online False-Discovery Control
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Control the institution-wide false-discovery burden as Contexts, hypotheses, models, and treatments arrive over time.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Ordered hypothesis stream.
- Exposure and trial ledger.
- Evidence budgets.

## Output contracts

- Allocated testing level.
- Discovery status.
- False-discovery wealth ledger.

## Algorithmic design

- Use predeclared online FDR/alpha-investing family appropriate to dependency assumptions.
- Group hypotheses by campaign and Context family.
- Spend more budget only through explicit institutional governance, not model excitement.
- Count retries, variants, feature ideas, and manual inspections.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Hypothesis ordering immutable after outcomes.
- Hidden tests isolated.
- No deletion of failed tests to restore wealth.

## Measurement system

- FDR wealth.
- Discoveries per budget.
- Exposure-adjusted hypothesis count.
- Family-wise sensitivity.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Every new model gets fresh alpha.
- Teams split one hypothesis into many.
- Negative trials omitted.

## UCEE integration

- None declared.

## Required tests and evidence

- Null campaign simulation.
- Adaptive ordering attack.
- Duplicate hypothesis detection.
- Dependency stress.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Complete_Trial_And_Exposure_Universe]]
- [[Hidden_Evaluation_Service_Architecture]]
