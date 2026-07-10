---
id: EXP0018-P06-INDEX
title: "P06 Host-Timeframe Close Confirmation v2 Index"
type: implementation-note
status: implemented
project: EXP0018
phase: P06
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - p06
  - confirmation
---

# P06 — Host-Timeframe Close Confirmation v2

## Mission

Convert live P05 one-sided hunt transitions into exactly one immutable outcome at the first eligible close of the Expert host timeframe.

## Reading order

1. [[01_SCOPE_AND_AUTHORITY]]
2. [[03_HOST_TIMEFRAME_CLOCK_CONTRACT]]
3. [[04_CANDIDATE_ADMISSION_CONTRACT]]
4. [[06_CONFIRMATION_STATE_MACHINE]]
5. [[07_CLOSE_EVALUATION_ALGORITHM]]
6. [[12_CAUSAL_AVAILABILITY_AND_AS_OF_TRUTH]]
7. [[13_MISSED_CLOSE_AND_FAIL_CLOSED]]
8. [[15_RESTART_CHECKPOINT_CONTRACT]]
9. [[20_TEST_AND_FIXTURE_PLAN]]
10. [[26_DEFINITION_OF_DONE]]

## Outputs

- pending confirmation candidates;
- immutable close outcomes;
- hunter-symbol host-bar geometry;
- deterministic events and audit rows;
- restart checkpoint state;
- read-only API for P07, P08, P11, and P12.
