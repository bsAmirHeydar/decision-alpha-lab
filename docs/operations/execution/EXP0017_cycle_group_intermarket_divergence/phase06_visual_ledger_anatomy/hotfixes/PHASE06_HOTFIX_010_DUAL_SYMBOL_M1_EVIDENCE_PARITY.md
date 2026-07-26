# Phase 06 Hotfix010 — Dual-Symbol M1 Evidence Parity

## Observed defect

The expert runs on `SPXUSD` but centrally evaluates and draws both `SPXUSD` and `NDXUSD`. The SPX chart could appear to respect reference freshness while the NDX chart still showed divergence legs tied to levels that were not proven fresh.

The defect was deeper than chart-object cleanup. The state engine accepted incomplete M1 evidence from the non-host symbol and then the renderer treated that state as authoritative.

## Root cause A — `InpRequireM1History` was not enforced

The configuration flag was propagated through the modules, but the reference and current-range aggregators treated any positive `CopyRates` result as complete data:

```text
copied > 0 => data_ok
```

For the host symbol, history is normally already warm. For the non-host symbol, MetaTrader can initially return an incomplete interval while history is still loading. A partial NDX interval can:

- miss a later high or low that consumed an older reference;
- miss an NDX touch inside the current CG;
- classify NDX as clean when it was not clean;
- create a false pair divergence and a false NDX companion line.

## Root cause B — end-boundary contamination

The current-cycle range and exact-extreme-time drawing query used the closed-candle boundary as an inclusive `CopyRates` endpoint. A bar opening exactly at the boundary belongs to the next observation interval.

This could make the logical price interval and the visual anchor interval disagree.

Hotfix010 standardizes all Phase 06 M1 windows as:

```text
[start, end)
CopyRates stop = end - 1 second
```

## Root cause C — missing later cycles were skipped

The frontier scan walks completed references from newest to oldest. Previously, a missing later reference cycle was ignored with `continue`.

That is not a valid freshness proof. If a later NDX interval is missing, an older NDX level cannot be declared unbroken because the intervening path is unknown.

Hotfix010 converts any missing newer pair into a frontier-history barrier. Every older candidate is suppressed until complete evidence exists.

## Root cause D — backfill finalized before NDX was ready

Historical backfill set its completion flag on the first pulse. If NDX history was still loading, the partial reconstruction became permanent until the expert was manually reattached.

Hotfix010 now:

1. collects the historical observation range;
2. checks that both configured symbols expose the required M1 history bounds;
3. waits and retries if either symbol is not ready;
4. resets confirmation/lifecycle state before deterministic replay;
5. clears all owned objects on both charts immediately before authoritative replay;
6. marks backfill complete only after the dual-symbol preflight passes.

## New invariants

### Reference interval invariant

When `InpRequireM1History=true`, every completed reference cycle must have:

```text
copied M1 bars == expected interval minutes
first bar time == interval start
last bar time == interval end - 60 seconds
no internal M1 timestamp gap
```

### Current-range invariant

The observed current CG range must satisfy the same complete-coverage contract up to the closed-candle boundary.

### Frontier invariant

```text
missing later reference evidence => older reference freshness is unproven => suppress
```

### Rendering invariant

A chart leg is drawable only when that exact chart symbol has:

```text
complete reference M1 data
complete current-range M1 data
fresh symbol-local frontier authority
```

In strict pair mode, both symbols must satisfy all three conditions before either chart receives a line.

## Scope

Modified logic:

- reference-cycle M1 aggregation;
- current-cycle M1 aggregation;
- frontier-history gap handling;
- historical backfill readiness;
- symbol-local drawing authority;
- exact visual extreme-time boundaries.

Unchanged:

- CG definitions;
- touch-only hunt doctrine;
- one-sided divergence doctrine;
- protected-reference retirement semantics;
- signal IDs;
- ledger schema;
- trading and risk execution.
