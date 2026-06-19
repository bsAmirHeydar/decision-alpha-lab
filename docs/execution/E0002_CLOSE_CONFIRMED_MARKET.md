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
