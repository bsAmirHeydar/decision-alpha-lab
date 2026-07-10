---
id: EXP0018-P06-MISSED
title: "P06 Missed Close and Fail-Closed Policy"
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

# Missed close

If the latest closed host bar advances by more than one expected interval, P06 cannot reconstruct the P05 state at each missed close from the latest aggregate snapshot. Every affected pending candidate becomes `MISSED_CLOSE_REPLAY_REQUIRED`.

No later state is backdated. P11 chronological replay is the only authorized reconstruction path.
