# Phase 14 Validation Plan

## Static contract checks

- Expert default trade leg is protected.
- `cg_3m` defaults true and every other CG defaults false.
- ATR defaults to period 14 and multiplier 1.0.
- Confirmation candle is copied from `[close - period, close)`.
- BUY stop uses candle low; SELL stop uses candle high.
- Signal source calls the existing `BuildFinalSignalsForGroup` authority.
- Warmup checks M1 bounds for Symbol A and Symbol B.
- Attempt registration occurs before planning and routing.
- Backtest-only runtime contains a tester gate.
- CTrade exists only in the router module.

## MetaEditor compile gate

Compile:

```text
EXP0017_CG_Raw_Execution_Backtest.mq5
```

Required result:

```text
0 errors, 0 warnings
```

## Strategy Tester scenarios

### Scenario A — default protected CG3

- only `cg_3m=true`;
- protected leg;
- verify every order comment begins with `E17|3m|P|`;
- verify BUY SL is below the protected confirmation candle low;
- verify SELL SL is above the protected confirmation candle high;
- verify TP distance equals one ATR within symbol rounding.

### Scenario B — hunter leg

- switch only `InpTradeLeg` to hunter;
- verify direction remains unchanged;
- verify candle, SL, ATR, TP, and volume are calculated on hunter symbol.

### Scenario C — duplicate suppression

- keep a confirmed signal visible across multiple closed bars;
- verify one signal ID produces one attempt only.

### Scenario D — restart warmup

- start test or attach expert after the New York trading day has begun;
- verify earlier signals are replayed without orders;
- verify protected-reference lifecycle matches a test started at 18:00 NY.

### Scenario E — secondary-symbol history delay

- withhold or delay NDX history;
- verify warmup does not complete and no order is sent;
- load NDX history and verify deterministic continuation.

### Scenario F — broker constraints

- test minimum volume, volume step, stop level, stale quote, and spread limit rejection paths;
- verify each rejection appears in the audit CSV.

## Acceptance

Phase14 v1 is accepted only after MetaEditor compilation and visual reconciliation of at least one BUY and one SELL plan against the selected trade symbol's exact confirmation candle.
