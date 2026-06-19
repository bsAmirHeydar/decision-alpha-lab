# EXE0002 — Close-Confirmed Market After Touch

This execution experiment is the second implementation of the H0005 reversal idea.
It is intentionally a separate EA:

```text
mql5/Experts/DecisionAlphaLab/Execution/E0002_CloseConfirmedMarket.mq5
```

It does not add a mode to `E0001_ReversalOneToOne.mq5`.

## Rule

When the effective regime is reversal:

1. Build H5 reversal node candidates from M0001/M0002.
2. Watch nearest LOW nodes below market and HIGH nodes above market.
3. Wait for the last closed candle to touch a candidate zone.
4. If the close does not break the far edge of the zone, enter at market.
5. Put SL behind the zone.
6. Put TP at the first opposite-node touch by default. `InpRewardR` is a reference/cap only if `InpUseFixedRExitIfCloser=true`.
7. Lock that node touch until a full zone exit and later revisit.

## Recommended default test settings

```text
InpTradingEnabled = true
InpRewardR = 1.0
InpBuyLimitSlots = 3
InpSellLimitSlots = 3
InpRefreshSetupsOnNewBarOnly = true
InpManageOrdersEveryTick = false
InpUseClosedBarsOnly = true
InpMagicNumber = 5002002
InpOrderCommentPrefix = DALR2
InpH5ReportEnabled = false
```


## TP policy

TP defaults to the first opposite-node touch. If `InpUseFixedRExitIfCloser=true`, the fixed-R target from `InpRewardR` may be used only when it is closer than that opposite touch. If `InpAllowOppositeTouchBelowRewardR=false`, setups whose opposite touch is below the configured R threshold are skipped.


## Build 1.03 performance defaults

The compile issue in market TP diagnostics is fixed. E0002 defaults to error-only logging and avoids repeated pending-order scans inside the normal close-confirmed market cycle.


## Minimal input surface

Release 1.26 / E0002 1.04 hides diagnostic and engine-maintenance knobs from the Strategy Tester input panel. Public inputs are limited to symbol/timeframe/bars, core H5 structure (`InpL`, `InpZoneRatio`, `InpExitGap`, `InpConsumeMode`), regime source, trading-session window, risk/target policy, near-node slots, and node revisit settings. Heavy reports, verbose logs, pending-maintenance flags, market-catch switches, and speed/runtime controls are fixed internally for faster and cleaner tests.

## Higher-timeframe regime filter

All four execution experts now support an optional higher-timeframe regime gate. The default is off, so existing tests are unchanged.

Inputs:

- `InpUseHigherTimeframeRegimeFilter` — enable/disable the higher-timeframe regime confirmation.
- `InpHigherRegimeTimeframe` — timeframe used for the higher-timeframe M0001/M0002 regime calculation, default `PERIOD_H1`.

Behavior:

- E0001 and E0002 require the higher timeframe to be `REVERSAL` before allowing reversal entries.
- E0003 and E0004 require the higher timeframe to be `CONTINUATION` before allowing continuation entries.
- The higher-timeframe filter is a gate only; it does not change node construction, touch locking, TP policy, or trade management.

