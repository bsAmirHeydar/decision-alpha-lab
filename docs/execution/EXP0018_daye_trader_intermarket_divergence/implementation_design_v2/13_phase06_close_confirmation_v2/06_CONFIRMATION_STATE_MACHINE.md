---
id: EXP0018-P06-STATE-MACHINE
title: "P06 Confirmation State Machine"
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

# State machine

```text
BASELINED SOURCE
      │ live transition to A_ONLY/B_ONLY
      ▼
PENDING CANDIDATE
      │ first target host close
      ├─ same one-sided role + source through close → CONFIRMED
      ├─ BOTH → INVALIDATED_DOUBLE_HUNT
      ├─ NONE → NO_SIGNAL_AT_CLOSE
      ├─ opposite role → INVALIDATED_ROLE_CHANGED
      ├─ unavailable or incomplete as-of evidence → UNAVAILABLE_AT_CLOSE
      └─ missed close → MISSED_CLOSE_REPLAY_REQUIRED
```

Final results are immutable. A later double hunt does not retract a previously confirmed result.
