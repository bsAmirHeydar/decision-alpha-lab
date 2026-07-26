---
title: "39 - Quota Consumption Explainer and Open Decision"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: open-decision
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 39 - Quota Consumption Explainer and Open Decision


## Why This Question Exists

The owner has already frozen **who owns the quota**: the earliest M1-hunt setup across both symbols and all relations in one A/L/N session. The remaining question is **when the quota becomes permanently spent** if the winning setup does not complete normally.

These moments are not equivalent:

| Stage | Meaning | What can still fail afterward? |
|---|---|---|
| `PLAN_CREATED` | Signal passed context, WW, quota arbitration, and preliminary geometry. | Quote can change, geometry can fail, order call can fail. |
| `ORDER_ATTEMPTED` | EA called the trade API. | Broker can reject, requote, timeout, or partially accept. |
| `ORDER_ACCEPTED` | Broker/platform accepted the order or position request. | Pending order can remain unfilled or be cancelled. |
| `FILLED` | A position or executed deal exists. | Post-fill management still occurs, but entry happened. |

## Option Effects

### A - Consume at plan creation

- Strongest one-shot behavior.
- Any later technical failure still burns the session.
- Simple and deterministic, but may discard the session because of a transient invalid quote.

### B - Consume at order attempt

- The first actual submission burns the session.
- Broker rejection still prevents another setup.
- Useful when "one attempt" is the intended rule.

### C - Consume at accepted order

- Geometry/pre-send failures release the reservation.
- A broker-accepted pending order consumes the session even if never filled.
- Often appropriate when order acceptance represents committed market participation.

### D - Consume at fill

- Rejected or unfilled orders do not consume the session.
- Requires a persistent reservation while the order is pending to prevent another signal from entering.
- More complex around partial fills, order cancellation, and session end.

### E - Two-stage reserve/consume/release

```text
AVAILABLE
  -> RESERVED when the earliest candidate wins
  -> CONSUMED at a chosen event (accepted order or fill)
  -> RELEASED only for explicitly allowed pre-consumption failures
```

This is the recommended architecture because it prevents races while preserving a configurable business rule. It still requires the owner to choose whether permanent consumption occurs at `ORDER_ACCEPTED` or `FILLED`, and which failure reasons are allowed to release the reservation.

## Required Owner Answer

Choose one canonical policy:

```text
A PLAN_CREATED
B ORDER_ATTEMPTED
C ORDER_ACCEPTED
D FILLED
E TWO_STAGE, consume at: ORDER_ACCEPTED or FILLED
  release on: [list exact reason codes]
```

## Safe Implementation Before Answer

The code may implement the full state machine and expose an enum, but the canonical live profile must set:

```text
quota_consumption_policy = UNSET
live_order_submission = DISABLED
```

Paper tests may exercise all policies. No one policy may be labelled owner-confirmed until a direct answer is received.

## Suggested Default, Not Yet Owner-Confirmed

```text
RESERVE atomically when earliest candidate wins
CONSUME on ORDER_ACCEPTED
RELEASE only on PRE_SEND_GEOMETRY_INVALID, QUOTE_UNAVAILABLE, or LOCAL_VALIDATION_FAILED
DO NOT RELEASE on broker rejection after a real order attempt unless owner explicitly chooses that behavior
```

## Authority Classification

| Classification | Meaning |
|---|---|
| `OWNER_CONFIRMED` | Explicitly selected by the owner in the 15-question decision response. |
| `SOURCE_CONFIRMED` | Directly present in the original Faerie Protocol source package or owner narrative. |
| `ARCHITECTURAL_DERIVATION` | Required to make the confirmed behavior deterministic, modular, testable, or compatible with shared cores. |
| `LEGACY_OBSERVATION` | Behavior observed in `FP 101.mq5`; not automatically canonical. |
| `OPEN_DECISION` | Must not be silently hard-coded. |

Canonical priority is: `OWNER_CONFIRMED` > `SOURCE_CONFIRMED` > reviewed `ARCHITECTURAL_DERIVATION` > `LEGACY_OBSERVATION`.

## Navigation

- [[00_EXP0019_MOC|EXP0019 Master MOC]]
- [[38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
- [[33_AMBIGUITY_AND_DECISION_REGISTER|Decision Register]]
- [[40_NORMATIVE_ALGORITHM_SPECIFICATION|Normative Algorithm Specification]]
- [[44_ACCEPTANCE_GATE_FOR_CODING|Acceptance Gate for Coding]]
