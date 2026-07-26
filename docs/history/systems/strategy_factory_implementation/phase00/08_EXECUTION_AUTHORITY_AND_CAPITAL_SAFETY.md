---
title: "Execution Authority and Capital Safety"
tags: [strategy-factory, phase-00, execution, capital-safety]
status: canonical
---

# Execution Authority and Capital Safety

## Audit result

The uploaded snapshot contains **zero identified executable order-send or order-check call sites**.

The repository imports `MetaTrader5` for market-data access, but the scan did not find:

- `mt5.order_send(...)`
- `mt5.order_check(...)`
- MQL5 `OrderSend(...)`
- MQL5 `OrderCheck(...)`
- `CTrade`

## Interpretation

This establishes the current authority baseline:

```text
Market-data read authority: present
Trade-decision authority: absent
Risk-allocation authority: absent
Order-construction authority: absent
Order-send authority: absent
```

## Why this boundary must remain explicit

A shared Strategy Factory will eventually contain modules that generate decisions and execution intents. Those capabilities are not equivalent to broker authority.

```text
AnatomyEvent
→ describes market state

ModelDecision
→ recommends or abstains

ActionPlan
→ proposes coordinated action

ExecutionIntent
→ requests an execution operation

BrokerAdapter
→ translates intent

OrderSend authority
→ changes capital state
```

Every transition must be explicit and independently auditable.

## Phase ownership

- Phase 00: scan and baseline.
- Phase 01: define authority-bearing contracts without implementation.
- Phase 16: define risk and action-plan limits.
- Phase 17: implement paper-only execution.
- Phase 18: implement MQL5/broker boundary under separate acceptance.

## Fail-closed rule

Any future audit finding of an executable order-send token outside the approved broker boundary changes the phase/release status to `BLOCKED` until classified.

## Mandatory rescan points

- before merging execution code;
- before paper-to-live promotion;
- before a release tag;
- after importing external strategy code;
- after changing MQL5 bridge packages.
