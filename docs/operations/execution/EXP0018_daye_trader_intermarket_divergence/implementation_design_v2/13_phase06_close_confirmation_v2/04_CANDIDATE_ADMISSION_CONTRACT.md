---
id: EXP0018-P06-ADMISSION
title: "P06 Candidate Admission Contract"
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

# Candidate admission

A candidate opens only when P06 has already baselined source state and then observes a transition into `A_ONLY` or `B_ONLY`.

## Not admissible

- a one-sided state already present on a fresh attach;
- `NONE`, `BOTH`, or `UNAVAILABLE`;
- observations already finalized;
- observations outside the live host horizon;
- blocked or unpublished P05 observations.

This prevents a fresh attach from fabricating the historical first confirming candle.
