---
id: EXP0018-P06-RESTART
title: "P06 Fresh Attach, Restart, and Warmup"
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

# Fresh attach

Existing source states are copied into source memory without opening candidates. This is a deliberate fail-closed warmup.

# Restart before close

Pending candidates are restored from a Common Files checkpoint. Their original first-seen time, roles, target host close, and latest source state remain intact.

# Restart after an unprocessed close

P06 does not use later state as if it were the close state. The candidate becomes `MISSED_CLOSE_REPLAY_REQUIRED`.
