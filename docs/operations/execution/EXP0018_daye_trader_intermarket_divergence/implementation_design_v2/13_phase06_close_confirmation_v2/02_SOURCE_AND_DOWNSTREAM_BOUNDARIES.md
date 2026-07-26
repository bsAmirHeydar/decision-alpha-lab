---
id: EXP0018-P06-BOUNDARY
title: "P06 Source and Downstream Boundaries"
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

# Boundaries

P06 embeds P05 and consumes only P05 contracts. It does not rescan chart highs and lows to invent a second hunt implementation.

Downstream consumers receive `DAYE_ConfirmationResult` snapshots. P07 may apply lifecycle policy only after a confirmed result. P08 may draw only confirmed results. P11 must replay the same state machine chronologically. P12 serializes the same identities.
