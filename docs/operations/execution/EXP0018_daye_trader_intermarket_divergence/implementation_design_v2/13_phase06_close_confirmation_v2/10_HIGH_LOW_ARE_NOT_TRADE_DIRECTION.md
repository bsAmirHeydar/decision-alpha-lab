---
id: EXP0018-P06-NO-DIRECTION
title: "P06 HIGH and LOW Are Not Trade Direction"
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

# No direction authority

P06 preserves `HIGH` and `LOW` from P05. It does not translate them into BUY or SELL while the doctrine ADR remains outside this phase. Consumers must not infer trade direction merely from P06 status.
