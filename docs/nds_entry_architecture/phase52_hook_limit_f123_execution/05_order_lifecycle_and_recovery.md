---
title: Phase 52 Order Lifecycle and Recovery
status: implemented
version: 1.0.0
updated: 2026-07-10
---
# Phase 52 Order Lifecycle and Recovery

## Pending lifetime

The pending order uses `ORDER_TIME_GTC`. It remains active until one of these events occurs:

- it is filled;
- its structural death/stop boundary is breached and cancellation is enabled;
- the operator removes it;
- broker/account conditions invalidate it.

## One attempt per Hook

The default contract allows one order attempt per Hook setup. The setup key contains:

```text
symbol
timeframe
Hook sequence id
Hook direction
origin time
terminal/resolve time
valid family
```

The consumed key is persisted in terminal GlobalVariables under account login and magic. Restarting the EA does not silently re-arm the same Hook.

The registry can be cleared explicitly with:

```text
InpNDSHookTradeResetUsedSetupsOnInit = true
```

This input must be returned to `false` after the intended reset.

## Paper mode

When the execution profile is enabled but live sending remains disabled, the module exports a `PAPER_LIMIT` decision and consumes the one-attempt registry. This is an order-decision audit, not a fill simulator. Full paper fills and lifecycle simulation remain a separate research adapter.

## Failure behavior

- rejected broker request: no setup-consumed marker is written;
- accepted order with no returned ticket: treated as failure and audited;
- close request accepted but ticket still open: treated as incomplete close;
- duplicate pending orders: deterministic reconciliation keeps the oldest;
- multiple positions: fail closed and require operator action.

## Ownership

Magic number is the broker-state authority. The short comment identifies family and sequence for human audit but is not used to decide whether an exposure is managed.
