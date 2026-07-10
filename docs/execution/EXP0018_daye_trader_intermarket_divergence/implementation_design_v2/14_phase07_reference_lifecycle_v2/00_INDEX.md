---
id: EXP0018-P07-INDEX
title: "P07 Reference Lifecycle and First-Sweep State Machine v2 Index"
type: implementation-note
status: implemented
project: EXP0018
phase: P07
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags: [exp0018, p07, lifecycle, first-sweep]
---
# P07 — Reference Lifecycle and First-Sweep State Machine v2

## Mission

Turn immutable P06 confirmations into lifecycle-governed historical uses while keeping a reference eligible only as long as the same protected symbol has not touched its own side of that reference.

## Reading order

1. [[01_SCOPE_AND_AUTHORITY]]
2. [[03_CANONICAL_POLICY_RESOLUTION]]
3. [[04_REFERENCE_AND_USE_IDENTITIES]]
4. [[05_REFERENCE_STATE_MACHINE]]
5. [[07_REPEAT_WHILE_PROTECTED_SURVIVES]]
6. [[08_PROTECTED_BREACH_RETIREMENT]]
7. [[10_FIRST_SWEEP_DEDUPLICATION_SCOPE]]
8. [[11_CAUSAL_PROCESSING_ORDER]]
9. [[14_RESTART_CHECKPOINT_CONTRACT]]
10. [[21_TEST_AND_FIXTURE_PLAN]]
11. [[27_DEFINITION_OF_DONE]]

## Outputs

- lifecycle records per reference period and side;
- immutable accepted-use records for P08 drawing;
- duplicate and rejected-use evidence;
- protected-touch, double-hunt, and role-switch retirement events;
- restart checkpoint state;
- read-only APIs for P08, P11, and P12.
