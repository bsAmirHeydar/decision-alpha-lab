# NDS F2 Fast Exact Backtest Hotfix — Audit Report

## Scope

This hotfix changes only the dedicated F2 Strategy Tester executable. The production Phoenix expert, Hook entry profile, NDS AI architecture and live-license path are not modified.

## Mechanical trade contract

```text
newly observable confirmed F2
→ bullish Buy Limit one trade tick below F2 waist
→ bearish Sell Limit one trade tick above F2 waist
→ Stop Loss at canonical parent F1 waist
→ Take Profit at F2 Leg2 endpoint
→ maximum one managed pending order or position
```

## Root causes corrected

### 1. False staleness

The former implementation measured setup age from `f2.confirm.time_anchor`. That timestamp belongs to the swing pivot, not the bar where the node became knowable. Since a confirmed node requires L right-side non-reaching candles, a genuinely fresh F2 could already appear several bars old and be blocked.

The hotfix reconstructs the exact right-clearance completion index. Equal-price touches are skipped exactly as in Phoenix Level 02. `MaxSetupAgeBars=0` now means the first bar on which the F2 can actually be known without lookahead.

### 2. Unnecessary full finalization

The prior tester called `FP_DetectAllScales`, which also runs F3 locking, global ownership, duplicate visual merging, Hook seed visibility, Level-11 canonical rendering checks and result recounting.

The new `FP_NDSF2FastDetector.mqh` reuses `FP_DetectScale` and all approved node/F1/F2 builders but stops before those non-execution passes.

### 3. Hook work in an F-only strategy

`cfg.scan_hooks` is now false and F1 roots use the canonical raw-origin fail-open path. No Hook branch is built or consumed.

### 4. Tester overhead

Removed from this runtime:

- all custom `Print` and `PrintFormat` calls;
- session/run timing and statistics;
- terminal Global Variable registry and flushes;
- global entry mutex;
- duplicate-pending reconciliation path;
- CSV, rendering, timer and chart-event paths.

The one-attempt registry is now in memory and reset per tester initialization when requested.

### 5. Broker request certainty

The order path now builds an explicit `MqlTradeRequest`:

```text
TRADE_ACTION_PENDING
ORDER_TYPE_BUY_LIMIT / ORDER_TYPE_SELL_LIMIT
ORDER_TIME_GTC
ORDER_FILLING_RETURN
SL = F1 waist
TP = F2 Leg2
```

`OrderCheck` is executed before `OrderSend`. A setup is marked used only after an accepted pending request or a verified managed exposure appears.

## Runtime profiles

### FAST

```text
420 closed bars
scales 2, 3, 5
900 event cap
Hook cap 0
```

### PARITY

```text
2500 closed bars
scales 2, 3, 5, 8, 13, 21
4000 event cap
Hook cap 0
```

## Validation completed

```text
NDS F2 fast contract QA: PASS
MQL5 compatibility: 0 errors, 0 warnings
Engineering policy: 0 errors, 0 warnings
Repository layout: 0 missing directories
AI Engineering OS vault: 0 errors, 0 warnings
MQL lexical balance: PASS
Expert include resolution: 0 missing includes
Custom runtime Print scan: 0 matches
```

MetaEditor and Strategy Tester are not available in the build environment. Final compile and broker-simulation confirmation must be performed locally.
