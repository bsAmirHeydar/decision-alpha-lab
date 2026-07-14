---
title: Build the Counterfactual Outcome Cube
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v3
  - runbook
  - operations
---

# Mission

Replay every occurrence-treatment sibling through executable paths and preserve fill, censoring, cost, trail, and ambiguity.

## Entry conditions

- Frozen occurrence clusters.
- Frozen treatment lattice.
- Bitemporal market and broker data.

## Mandatory roles and separation of duties

- Replay engineer.
- Data-quality owner.
- Execution auditor.
- Independent validator.

## Procedure

1. Freeze data snapshot and economics profile.
2. Run point-in-time event reconstruction.
3. Simulate triggers, fills, partial fills, cancellations, stops, targets, trails, expiries, and invalidations.
4. Resolve or bound path ambiguity.
5. Store non-fill and opportunity cost.
6. Reproduce sample paths independently.

## Mandatory outputs

- Outcome cube.
- Path/event ledgers.
- Ambiguity report.
- Cost attribution.

## Stop and escalation conditions

- Data quality quarantine.
- Same-bar ambiguity unresolved and unbounded.
- Replay mismatch.
- Future specification detected.

## Evidence retained

- Raw/canonical data hashes.
- Replay code/environment.
- Differential evidence.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Counterfactual_Outcome_Cube_V3]]
- [[Path_Dependent_Trailing_Truth_Engine]]
