# E0002 — H0005 Close-Confirmed Market Executor

`E0002_CloseConfirmedMarket.mq5` is a separate Expert Advisor from `E0001_ReversalOneToOne.mq5`.
It does **not** add a mode to E0001 and does not modify the limit-on-touch executor.

## Execution contract

E0002 uses the same hypothesis modules as the rest of Decision Alpha Lab:

- M0001 structural nodes/events are the source of zones and node lifecycle.
- M0002 completed branch samples are the source of reversal/continuation regime.
- The optional human-context input can override or block the completed-branch regime gate.

On each new closed candle, if the effective regime is reversal, E0002 checks the nearest active H5 reversal nodes:

- LOW nodes below market are buy candidates.
- HIGH nodes above market are sell candidates.
- Default candidate caps are 3 buy-side nodes and 3 sell-side nodes.

## Close-confirmed market entry

E0002 does not park pending limits.
It waits for a closed candle to touch a node zone and then confirms that the close did not break the far edge of the zone.

### Buy from LOW node

A buy signal is valid when:

```text
bar_low <= zone_upper
bar_close > zone_lower
```

The market order is sent on the next tick/bar processing pass:

```text
entry = current ask
SL    = zone_lower
risk  = entry - SL
Fixed-R cap     = entry + risk * InpRewardR
Opposite target = first HIGH-node touch edge above entry
TP              = Opposite target by default; if InpUseFixedRExitIfCloser=true and Fixed-R cap is closer, use Fixed-R cap
```

### Sell from HIGH node

A sell signal is valid when:

```text
bar_high >= zone_lower
bar_close < zone_upper
```

The market order is sent on the next tick/bar processing pass:

```text
entry = current bid
SL    = zone_upper
risk  = SL - entry
Fixed-R cap     = entry - risk * InpRewardR
Opposite target = first LOW-node touch edge below entry
TP              = Opposite target by default; if InpUseFixedRExitIfCloser=true and Fixed-R cap is closer, use Fixed-R cap
```

TP defaults to the first opposite-node touch using the actual market-entry risk only for R diagnostics. If `InpUseFixedRExitIfCloser=true`, E0002 may exit at `InpRewardR` only when that target is closer than the opposite touch. If `InpAllowOppositeTouchBelowRewardR=false`, E0002 skips market entries whose opposite touch is below the configured R threshold.

## Touch/revisit ledger

The node-zone ledger prevents duplicate entries inside the same touch episode.
After a node touch signal is processed, the node is locked until price exits the full zone with `InpTouchRevisitResetBufferPoints`.
Only after that full zone exit can a later return become a revisit and trigger a new E0002 market attempt.

## Session behavior

If `InpUseTradingSessionFilter=true`, E0002 works only inside the configured broker-time or GMT session.
Outside the session:

- no market signal is executed;
- any managed pending limits with E0002 prefix/magic are force-deleted as a safety cleanup;
- open positions are not force-closed and remain governed by their own SL/TP.

## Managed identity

Defaults are separate from E0001:

```text
InpMagicNumber = 5002002
InpOrderCommentPrefix = DALR2
```

This allows E0001 and E0002 to be tested separately without mixing managed orders.


## Build 1.03 compile and speed fix

Build 1.03 fixes the close-confirmed market diagnostic compile error from undeclared `tp_model`, `fixed_r_tp`, and `opposite_touch_r` variables. Market-entry TP diagnostics are now returned by the order helper and printed only when order diagnostics are enabled or a real send fails with error logging enabled.

E0002 remains a pure market-after-close Expert. It no longer scans/deletes managed pending orders on every signal pass; pending cleanup is reserved for startup/session-close guards. Default logging is `DAL_EXEC_LOG_ERRORS` for faster Strategy Tester runs.


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

