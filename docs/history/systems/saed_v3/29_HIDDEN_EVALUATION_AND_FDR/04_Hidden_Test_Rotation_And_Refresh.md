---
title: Hidden Test Rotation and Refresh
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Maintain long-term validity of protected evaluation as markets, feeds, Contexts, and research exposure evolve.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Contamination risk.
- Data arrival.
- Domain coverage.

## Output contracts

- Test generation plan.
- Retired and active protected sets.

## Algorithmic design

- Use rolling sealed cohorts and never recycle exposed rows into fresh hidden tests.
- Stratify by regime, symbol, session, broker economics, and Context support.
- Reserve future accrual for truly prospective evaluation.
- Document test-set age and contamination risk.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Refresh process independent from model teams.
- No cherry-picking favorable periods.
- Retired tests retained for audit but not current selection.

## Measurement system

- Test age.
- Coverage.
- Contamination probability.
- Refresh cadence.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Same final test used for years.
- Refresh after poor result.
- New test overlaps training events.

## UCEE integration

- None declared.

## Required tests and evidence

- Overlap scan.
- Temporal isolation.
- Coverage comparison.
- Contamination audit.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Protected_Evidence_Access_And_Blinding]]
- [[Prospective_Challenge_Protocol]]
