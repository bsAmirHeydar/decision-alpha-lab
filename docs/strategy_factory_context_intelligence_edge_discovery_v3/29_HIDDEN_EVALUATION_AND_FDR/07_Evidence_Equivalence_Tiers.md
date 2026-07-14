---
title: Evidence Equivalence Tiers
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Define what it means to reproduce a research result across hardware, libraries, languages, and runtime targets.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Reference and replica artifacts.

## Output contracts

- Bitwise, prediction, decision, and evidence equivalence states.

## Algorithmic design

- Tier 1 bitwise equality where deterministic kernels permit.
- Tier 2 prediction equivalence under declared tolerance.
- Tier 3 decision equivalence after calibration/policy.
- Tier 4 evidence equivalence for statistical conclusions and gates.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Lower tier cannot be mislabeled higher.
- Tolerance set before comparison.
- Decision changes receive severity classification.

## Measurement system

- Equivalence tier achieved.
- Decision mismatch rate.
- Metric drift.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Similar Sharpe treated reproduction.
- Tolerance widened after mismatch.
- Rare tail decisions ignored.

## UCEE integration

- None declared.

## Required tests and evidence

- Boundary-value parity.
- Float precision shift.
- Ordering nondeterminism.
- Language export.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Independent_Replication_Program]]
- [[Runtime_Compilation_And_MQL5_Parity]]
