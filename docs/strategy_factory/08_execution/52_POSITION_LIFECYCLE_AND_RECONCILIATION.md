---
type: strategy-factory-document
status: canonical
title: "Position Lifecycle and Reconciliation"
tags:
  - strategy-factory
---

# Position Lifecycle and Reconciliation

Execution is a state machine that must survive terminal restarts, network failure, partial fills, and manual broker changes.

## States

Intent created, risk reserved, submitted, accepted, pending, partially filled, filled, managed, closing, closed, cancelled, rejected, orphaned, and quarantined. Allowed transitions are explicit.

## Reconciliation

On startup and periodically, compare local intents, orders, deals, and positions with broker truth. Unknown broker positions or missing local state stop automation and require incident resolution.

## Idempotency

Intent IDs and broker comments provide stable idempotency keys. Reprocessing an event or restart cannot create a second order. Lifecycle updates are append-only.

