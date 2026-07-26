---
title: Bitemporal Context Truth and Suffix Invariance
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Guarantee that every Context feature and decision can be reconstructed exactly from information available at decision time, despite later data revisions.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Event-time feed.
- System-time ingestion and revision ledger.
- Context lifecycle events.

## Output contracts

- Bitemporal Context snapshots.
- Suffix-invariance certificate.

## Algorithmic design

- Store valid_time and system_time for every fact.
- Generate as-known-at snapshots by deterministic temporal joins.
- Run future-suffix mutation: alter all events after decision time and require unchanged pre-decision Context, features, candidates, and decisions.
- Represent corrections as new versions; never overwrite historical decision-time truth.

## Formal objective and constraints

```text
snapshot(t_decision, t_system) = {facts | valid_time <= t_decision and system_time <= t_system}
```

## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No latest-value join in research or runtime.
- Preprocessing fit respects role and time.
- Revision-aware transport tests across vendors.

## Measurement system

- Suffix-invariance pass rate.
- Revision impact rate.
- As-known-at reconstruction latency.
- Temporal leakage incidents.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Revised OHLC rewrites historical Context.
- Calendar or symbol mapping uses future state.
- Feature window crosses decision time.

## UCEE integration

- None declared.

## Required tests and evidence

- Random suffix perturbation.
- Late-arrival replay.
- Clock-shift and DST mutation.
- Vendor correction differential.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Data_Contract_And_Bitemporal_Truth]]
- [[Temporal_Leakage_Attack_Library]]
