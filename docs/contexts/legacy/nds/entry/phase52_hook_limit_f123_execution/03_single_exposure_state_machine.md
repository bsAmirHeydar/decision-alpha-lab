---
title: Phase 52 Single Exposure State Machine
status: implemented
version: 1.0.0
updated: 2026-07-10
---
# Phase 52 Single Exposure State Machine

## Hard contract

Phase 52 permits at most one managed exposure for its magic number across all charts and symbols:

```text
managed pending orders + managed open positions ≤ 1
```

Ownership is based on `magic`, not broker comments. Comments remain audit metadata and are not trusted as the primary ownership key.

## State machine

```text
DISABLED
  └─ no action

IDLE
  ├─ no eligible Hook → IDLE
  ├─ eligible Hook but blocked geometry → BLOCKED
  └─ eligible Hook + authority → LIMIT_PENDING

LIMIT_PENDING
  ├─ unfilled and alive → hold
  ├─ death/stop boundary breached → cancel → IDLE
  └─ filled → POSITION_OPEN

POSITION_OPEN
  ├─ no post-entry same-direction F123 → hold
  ├─ protective stop executed by broker → IDLE
  └─ qualifying F123 completes → market close → IDLE
```

## Multi-chart race prevention

A terminal GlobalVariable compare-and-swap lock is acquired immediately before the final exposure re-check and order submission. This closes the race where two chart instances could both observe an empty account state and submit simultaneously.

Lock identity:

```text
account login + strategy magic
```

A short stale timeout prevents a crashed instance from blocking future entries indefinitely.

## Recovery invariants

- If a position exists, all managed pending orders are deleted.
- If duplicate managed pending orders are found, the oldest is kept and extras are deleted.
- If more than one managed position already exists, the engine fails closed and requires manual reconciliation; it does not guess which live position to liquidate.
- A position on the current symbol with another magic blocks entry to avoid netting-account contamination.
