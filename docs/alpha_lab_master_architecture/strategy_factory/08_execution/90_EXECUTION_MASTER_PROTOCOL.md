---
type: strategy-factory-reference
status: canonical
title: "Execution Master Protocol — Paper, Micro-Live, and Live"
tags:
  - strategy-factory
  - execution
  - risk
  - reference
---

# Execution Master Protocol — Paper, Micro-Live, and Live

## Purpose

The execution protocol ensures that a validated research decision becomes exactly one bounded broker action and that actual broker state remains observable and reconcilable. Execution is treated as a safety-critical state machine, not a final utility function.

## End-to-end live path

```text
closed market update
 -> anatomy event/update
 -> immutable snapshot
 -> candidate generation
 -> rule/model decision
 -> candidate compatibility check
 -> hard risk evaluation
 -> risk reservation
 -> broker preflight
 -> request submission
 -> response/fill trace
 -> position management
 -> close/reconciliation
 -> risk release
 -> monitoring and research comparison
```

Every arrow emits a reason-coded trace. Skips are recorded as decisions; they are not missing data.

## Decision timing

The runner uses a declared clock and closed-bar/intrabar contract. Stale decisions expire. A model decision must be produced before the candidate expires and inside the maximum latency. System-clock, broker-clock, exchange-clock, and UTC discrepancies are monitored.

## Risk reservation

Risk is reserved before order submission to prevent concurrent intents from exceeding limits. Reservation uses worst-case initial risk including expected costs and gap policy where appropriate. Partial fills reserve proportional risk plus remaining pending exposure. Cancellation releases pending reservation only after broker confirmation or reconciliation.

## Broker preflight

Validate:

- symbol selected and synchronized;
- market/session open;
- latest bid/ask age;
- order type allowed;
- entry, stop, and target normalized to tick size;
- stop/freeze distance;
- volume min/max/step;
- point/tick value and currency conversion;
- margin and account mode;
- expiration support;
- duplicate intent/comment/magic;
- existing correlated exposure;
- risk state and kill switch.

Preflight failure records the exact constraint and never attempts a “close enough” order.

## Idempotent submission

`intent_id` is the idempotency key. Before sending, search local trace and broker orders/positions. A timeout does not imply failure; reconcile using intent metadata before retry. A second send is prohibited until the first request is resolved.

## Order and position states

```text
created
 -> risk_reserved
 -> preflight_passed
 -> submitted
 -> accepted/pending
 -> partially_filled
 -> filled
 -> managed
 -> closing
 -> closed
```

Terminal alternatives: rejected, cancelled, expired, orphaned, quarantined. Every transition has timestamp, source, reason, and broker identifiers.

## Fill and slippage accounting

Use actual fill price and volume. Calculate expected versus realized spread/slippage in price, ticks, currency, and R. Partial fills have weighted price and remaining order state. Excessive slippage can cancel remaining volume or activate a kill policy according to the manifest.

## Position management

Management policies are deterministic plugins. State changes—partial close, stop move, target move, time exit—must use information known at transition time. The position keeps its original candidate and intent identity. Manual broker changes are detected and classified; automation may stop managing until an operator resolves ownership.

## Restart recovery

At startup:

1. load append-only local intent/trace state;
2. query broker orders, deals, and positions;
3. map by account, symbol, magic, comment, order/deal IDs, and intent ID;
4. rebuild open risk from broker truth;
5. identify orphaned or duplicate state;
6. refuse new orders until hard mismatches are resolved.

No in-memory-only state is authoritative.

## Paper parity

The paper broker accepts the same intent and risk gate. It uses live quotes or a documented fill model, persists state, and supports restart. Research and paper differ because paper has real-time availability, latency, and feed conditions. Paper is complete only when traces reconcile with expected decisions.

## Micro-live

Micro-live uses tiny fixed risk and a restrictive allowlist. Objectives:

- verify event and feature parity;
- measure decision latency;
- measure broker reject/fill/slippage;
- test restart and reconciliation;
- compare model calibration and outcome;
- exercise kill switch.

Income is not the objective. Risk is not increased after a short favorable run.

## Hard kill switches

Global or strategy-level kill conditions include:

- data/clock stale;
- feature/model/schema hash mismatch;
- unknown or missing candidate policy;
- risk-state reconstruction failure;
- duplicate intent;
- broker/account mode change;
- repeated rejection/timeout;
- slippage/cost beyond tolerance;
- daily loss/open risk breach;
- event or decision rate anomaly;
- manual operator stop.

Kill means no new exposure. Existing positions follow the predeclared emergency management policy.

## Audit and monitoring

Store:

- event and snapshot hashes;
- candidate set and selected candidate;
- rule/model decision and explanation;
- risk gate inputs and result;
- normalized request;
- broker response and all transitions;
- realized costs and PnL;
- latency at each stage;
- software/model/config versions.

Monitoring distinguishes health, execution quality, risk, and economic drift. A losing trade is not a technical incident; a missing stop or mismatched position is.

## Live adapter acceptance

The patch deliberately provides only interfaces and paper logic. A live MQL5 adapter must pass MetaEditor compilation, Strategy Tester dry runs, broker demo tests, reject/timeout/restart fixtures, and a separately approved promotion. It must not modify anatomy or model output.
