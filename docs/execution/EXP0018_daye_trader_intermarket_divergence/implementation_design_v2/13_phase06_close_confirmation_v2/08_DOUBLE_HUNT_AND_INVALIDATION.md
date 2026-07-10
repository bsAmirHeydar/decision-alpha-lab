---
id: EXP0018-P06-DOUBLE-HUNT
title: "P06 Double Hunt and Invalidation"
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

# Double hunt

A candidate can appear early in a host candle and become `BOTH` before the candle closes. P06 evaluates the final source state available through close. `BOTH` produces `INVALIDATED_DOUBLE_HUNT` and never a confirmed output.

A different relationship or the opposite side in the same candle remains independent.
