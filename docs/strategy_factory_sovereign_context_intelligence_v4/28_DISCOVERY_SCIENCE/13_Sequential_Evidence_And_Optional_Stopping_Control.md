---
title: Sequential Evidence and Optional-Stopping Control
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Allow long-running research and prospective monitoring without invalid inference from repeated peeking or adaptive stopping.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Sequential outcomes.
- Predeclared monitoring plan.
- Alpha/evidence budget.

## Output contracts

- Anytime-valid evidence state.
- Stopping or continuation decision.

## Algorithmic design

- Use confidence sequences, e-values, alpha-spending, or predeclared group-sequential boundaries where assumptions fit.
- Separate safety monitoring from efficacy claims.
- Record every peek, dashboard exposure, and adaptive decision.
- Reset evidence when policy changes materially.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No conventional p-value after repeated peeking.
- Safety stop may occur anytime; promotion stop follows predeclared rule.
- Agent monitoring counts as exposure.

## Measurement system

- Type-I budget spent.
- Expected stopping time.
- Safety detection delay.
- Exposure count.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Paper run stopped when curve looks good.
- Multiple dashboards treated informal.
- Policy tuned mid-run.

## UCEE integration

- None declared.

## Required tests and evidence

- Null sequential simulation.
- Unrecorded peek detection.
- Boundary crossing.
- Policy-change reset.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Online_False_Discovery_Control]]
- [[Prospective_Challenge_Protocol]]
