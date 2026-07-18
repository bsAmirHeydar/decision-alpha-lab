---
title: ACL-06 — Research DAG Orchestration
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-06]
---
# ACL-06 — Research DAG Orchestration

## Status

Accepted reference implementation. Claim ceiling: `BOUNDED_RESEARCH_EXECUTION_REFERENCE_ONLY`.

## Upstream dependency

ACL-06 consumes only a byte-valid `ACL05_TO_ACL06` handoff and the exact immutable generated root it identifies. The frozen Batch, setup behavior, search space, dataset cuts, labels, split, environment and budget cannot be repaired or expanded in place.

## Implemented responsibility

- closed-world task registry;
- deterministic DAG planning and acyclicity proof;
- stable task and cache identities;
- bounded idempotent execution;
- known-time-safe synthetic reference adapter;
- per-segment and per-candidate descriptive evidence;
- explicit research/diagnostic lane separation;
- deterministic resource accounting;
- immutable run artifact store;
- task receipts, event chain and provenance;
- atomic publication and replay verification;
- non-promotional `ACL06_TO_ACL07` handoff.

## Non-ownership

ACL-06 does not own inferential validation, multiple-testing control, robustness promotion, runtime trading, broker parity or capital authorization. ACL-07 must independently validate all evidence.

## Reference DAG

The reference run contains 54 tasks: four shared preparation tasks, 36 candidate-segment evaluations, 12 candidate aggregations, one result packaging task and one ACL-07 handoff task. All 12 frozen candidates are evaluated; the single diagnostic candidate remains non-selectable.

## Failure semantics

Unknown task types, digest mismatches, cycles, budget breaches, future leakage outside the diagnostic lane, missing receipts or publication conflicts fail closed. Partial results are never presented as a completed run.

## Claim boundary

Passing ACL-06 proves deterministic bounded orchestration against synthetic reference data only. It does not prove alpha, external data quality, statistical validity, MQL5 parity, live execution correctness or deployability.

## Related

[[ACL_05_IMMUTABLE_BATCH_AND_STORE]], [[ACL_07_UNIFIED_VALIDATION_GATE]], [[ACL06_RESEARCH_DAG_RUNTIME]], [[ACL06_ACL07_HANDOFF]]
