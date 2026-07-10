---
id: EXP0018-P06-HOSTILE
title: "P06 Hostile Review and Known Limitations"
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

# Hostile review

## Known limitation: fresh attach

Without prior state, P06 cannot prove when an already one-sided observation first appeared. It baselines rather than fabricates.

## Known limitation: timer downtime

If a close is missed, latest aggregate P05 state is insufficient for exact reconstruction. Outcome is replay-required.

## Known limitation: P05 aggregate availability

Exact first touch timestamp is still not claimed. P06 needs only the live transition observed by its own source memory.

## Known limitation: checkpoint scope

Checkpoint retains pending and finalized identity state, not the entire historical result ledger. Historical restoration belongs to P11/P12.
