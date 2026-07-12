# 06 — Module Architecture

## Runtime graph

```text
NDSF2WaistLimitBacktest.mq5
  └─ FP_NDSF2WaistBacktestEngine.mqh
      ├─ FP_Timebase.mqh
      ├─ FP_NodeScaleList.mqh
      ├─ FP_NDSF2FastDetector.mqh
      │   └─ canonical Phoenix node/F1/F2 builders
      └─ FP_NDSF2WaistTradeEngine.mqh
          └─ FP_NDSF2WaistTradeRules.mqh
              ├─ FP_NDSF2WaistBreakSetupRules.mqh
              ├─ FP_NDSF2WaistTradeTypes.mqh
              └─ shared Phase-52 sizing/broker helpers
```

## Responsibilities

### Expert

- input mapping;
- tester-only guard;
- once-per-new-bar scheduling;
- no custom print path.

### Fast detector

- canonical rates and nodes;
- F1 lifecycle;
- F2 body and lifecycle;
- no Hook construction in the entry-timeframe detector;
- optional HTF filter uses a separate cached canonical F/Hook classifier;
- no F3;
- no renderer or canonical visual ownership.

### Setup rules

- F2 body readiness;
- Point-1 / Point-2 mapping;
- direct parent F1 validation;
- body observability;
- entry, stop and target geometry;
- body-version identity.

### Trade rules

- one-attempt registry;
- volume calculation reuse;
- broker `OrderCheck` and `OrderSend`;
- managed exposure count;
- stale pending removal.

### Trade engine

- choose one latest candidate;
- paper/live tester mode;
- fail-closed execution.

## Deliberately excluded runtime layers

- Hook detection and validity;
- Zone engine;
- CG calendar;
- AI advisory;
- chart objects;
- CSV export;
- timer and chart events;
- F3 building;
- production license path.
