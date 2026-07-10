# Phase 14 — One-Shot Execution State Machine

## Purpose

This state machine formalizes the lifecycle of one divergence execution entitlement.

## States

```text
UNSEEN
  No canonical entitlement key exists in the registry.

CONSUMED
  The first eligible closed-candle observation has claimed the entitlement.
  This state is terminal for the trading day.
```

The current implementation intentionally has no retry, released, or rearmed state.

## Transition

```text
UNSEEN
  -- first confirmed observation -->
CONSUMED
```

All later observations remain in `CONSUMED` and are suppressed.

## Execution sequencing

```text
BuildConfirmedSignals(T)
        ↓
BuildTradeEntitlementKey(signal)
        ↓
Registry.Contains(key)?
   ├─ yes → audit suppression → stop
   └─ no  → append CONSUMED record
                         ↓
                  TradePlanner.Build
                         ↓
                  OrderRouter.Execute
```

The record append occurs before the planner. Consequently, every downstream result is terminal with respect to that divergence entitlement.

## Record anatomy

`SCGXTradeEntitlementRecord` stores:

- `entitlement_key`;
- original `signal_id` for traceability;
- CG name and duration;
- divergence side;
- New York trading-day start;
- current-cycle start;
- reference-cycle start;
- first observed lower-candle close;
- terminal state.

The first-observation close is metadata only. It is not part of identity.

## Restart reconstruction state machine

```text
EA init
  ↓
Collect closed boundaries for current NY trading day
  ↓
Replay each boundary through confirmation authority
  ↓
Build canonical entitlement keys
  ↓
Consume each first historical observation in registry
  ↓
Prime live clock
```

No call to `CCGX_OrderRouter::Execute()` is permitted during warmup.

## Failure semantics

| Failure location | Entitlement after failure | Later-candle retry |
|---|---:|---:|
| Key construction | Not consumed; signal rejected because identity is invalid | No valid execution path |
| Registry capacity | Not inserted; gate fails closed | Rejected again until corrected |
| Planner | Consumed | Forbidden |
| Position policy | Consumed | Forbidden |
| Paper acceptance | Consumed | Forbidden |
| Broker rejection | Consumed | Forbidden |
| Successful order | Consumed | Forbidden |

## Concurrency scope

The Phase 14 expert is designed to run as one execution owner for the configured pair. The in-process gate is deterministic for tester replay, ordinary ticks, repeated `Pulse()` calls, and same-day restarts reconstructed through warmup.

Attaching multiple independent executor instances to the same account is outside the current ownership contract and must not be used as a way to bypass one-shot semantics.

## Extension rule

Any future entry model must consume the same entitlement before it schedules, places, or retries an order. Entry-model modularity does not create additional trade permissions.

## Related documents

- [[PHASE14_ONE_SHOT_SIGNAL_EXECUTION_CONTRACT]]
- [[PHASE14_ONE_SHOT_VALIDATION_PLAN]]
- [[PHASE14_MODULE_ARCHITECTURE]]
