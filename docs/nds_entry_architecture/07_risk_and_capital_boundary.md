---
title: NDS Risk and Capital Boundary
status: normative
version: 1.0.0
---
# NDS Risk and Capital Boundary

## 1. Four separate authorities

```text
Analytical authority: is the NDS structure valid?
Setup authority: does the Zone create a tradable contract?
Risk authority: may capital be allocated, and how much?
Execution authority: may a broker instruction be transmitted now?
```

No earlier authority implies a later one.

## 2. Required future risk gates

Before volume can be non-zero, the system must check:

- maximum risk per plan;
- maximum risk per NDS family;
- maximum simultaneous NDS plans;
- aggregate symbol and correlated-index exposure;
- daily loss and drawdown limits;
- spread and slippage ceilings;
- margin sufficiency;
- stop-distance and freeze-level constraints;
- event/news or session policy, if approved;
- duplicate/replace semantics;
- stale quote and market-state checks;
- license and deployment profile;
- manual arm and kill switch.

## 3. Failure handling

A future execution layer must define states for:

```text
REQUEST_CREATED
REQUEST_VALIDATED
REQUEST_REJECTED
REQUEST_SENT
REQUEST_ACCEPTED
REQUEST_PARTIALLY_FILLED
REQUEST_FILLED
REQUEST_CANCELLED
REQUEST_EXPIRED
REQUEST_REPLACED
REQUEST_BROKER_ERROR
POSITION_RECONCILIATION_REQUIRED
```

## 4. Stop is not merely a numeric field

The final stop contract must distinguish:

```text
structural invalidation
broker stop price
emergency catastrophic stop
soft thesis exit
Zone death
position-management stop
```

Conflating these would destroy research attribution and live-risk clarity.

## 5. Current implementation

The current NDS Entry Transition package has no capital authority. Volume and risk fraction remain zero under every profile.
