---
title: Prospective Challenge Protocol
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Run a frozen, untuned, forward-only challenge that measures expected versus observed decisions, fills, costs, and outcomes.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Signed candidate generation.
- Frozen prospective plan.
- Live-arriving market events.

## Output contracts

- Prospective evidence dossier.
- Deviation and incident ledger.

## Algorithmic design

- Freeze Context, features, model, calibration, policy, treatments, costs, risk limits, and runtime generation.
- Record all opportunities, including Skip, Abstain, non-fill, reject, and missing data.
- Use sequential safety monitoring but predeclared efficacy analysis.
- No retraining, retuning, or threshold change.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Operational fixes that affect decisions create new version.
- Missing days cannot be silently dropped.
- Human override recorded and excluded/attributed per plan.

## Measurement system

- Decision agreement.
- Calibration.
- Expected-observed utility.
- Fill/cost deviation.
- Incident rate.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Policy changes mid-paper.
- Bad feed periods removed.
- Only traded opportunities retained.

## UCEE integration

- None declared.

## Required tests and evidence

- Freeze-hash audit.
- Opportunity completeness.
- Clock/restart reconciliation.
- Sequential stopping compliance.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Paper_Trading_Protocol]]
- [[Sequential_Evidence_And_Optional_Stopping_Control]]
