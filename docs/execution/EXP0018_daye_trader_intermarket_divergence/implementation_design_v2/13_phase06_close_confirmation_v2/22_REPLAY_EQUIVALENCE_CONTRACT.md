---
id: EXP0018-P06-REPLAY
title: "P06 Replay Equivalence Contract"
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

# Replay equivalence

P11 must feed chronological P05 transitions and host closes through the same pure candidate and finalization functions. Replay may reconstruct history because it possesses as-of source snapshots. Live P06 cannot replace replay with current aggregate state.

For identical event order, candidate IDs, result IDs, outcomes, roles, and endpoint geometry must match.
