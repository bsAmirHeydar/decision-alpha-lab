# 02 - Normalized Strategy Specification

## 1. Strategy identity

Strategy ID: `EXEC001_STC_SMT_CYCLES`

Strategy family: Intermarket divergence execution.

Primary signal type: SMT divergence between two index symbols.

Default symbols:

- Symbol1: `SPXUSD`
- Symbol2: `NDXUSD`

The same logic applies to equivalent pairs such as `SPX/NDX`, `US500/NAS100`, `ES/NQ`, or broker-specific equivalents. The code must treat `Symbol1` and `Symbol2` as both data symbols and execution symbols for this strategy version.

## 2. Runtime independence

The EA may be attached to any chart. The chart symbol does not define the strategy universe. All analysis and execution use only `Symbol1` and `Symbol2`.

The EA must block duplicate active instances for the same strategy ID and symbol pair. This prevents double entries if the user accidentally attaches the same EA to multiple charts.

## 3. Trading day

The STC trading day is defined in New York time.

- Start: 20:00 New York.
- End: 15:30 New York on the following calendar day.
- Hard reset: 15:30 New York.

No signal decision may use any data before the current STC trading-day start. Data from calendar yesterday may be valid if it belongs to the current STC trading day after 20:00 New York.

## 4. M cycles and no-entry gaps

The strategy has three M cycles:

- M1: 20:00 to 02:00.
- M2: 03:00 to 09:00.
- M3: 09:30 to 15:30.

The gaps are:

- 02:00 to 03:00.
- 09:00 to 09:30.

During gaps:

- No new divergence is detected.
- No entry is allowed.
- Open positions are still managed.
- If SL or TP is hit, position management records the event.
- If hard close or delayed partial becomes due, management continues.

## 5. W cycles

Each M has four W cycles. Every W is a synthetic 90-minute candle. The W high and W low may be built from any lower timeframe because the final high and low of the 90-minute window should be the same as long as the data coverage is complete.

W cycles are defined in New York time and anchored to their parent M.

M1:

- W1: 20:00-21:30.
- W2: 21:30-23:00.
- W3: 23:00-00:30.
- W4: 00:30-02:00.

M2:

- W1: 03:00-04:30.
- W2: 04:30-06:00.
- W3: 06:00-07:30.
- W4: 07:30-09:00.

M3:

- W1: 09:30-11:00.
- W2: 11:00-12:30.
- W3: 12:30-14:00.
- W4: 14:00-15:30.

## 6. Reference matrix

W1 never gives a signal.

W2 may compare only against W1.

W3 may compare only against W2 and W1.

W4 may compare only against W3, W2, and W1.

The current W never compares against itself.

References are always inside the same M. No W from a previous M and no W from a previous STC trading day may be used as a reference.

## 7. Structural two-symbol comparison

Each symbol owns its own W levels.

The strategy does not compare SPX price to NDX price. It compares structural events:

- Did Symbol1 hunt its own reference W high or low?
- Did Symbol2 hunt its own corresponding reference W high or low?

If exactly one symbol hunts and the other does not, SMT divergence exists.

## 8. Hunt definition

Hunt is touch-only.

High hunt:

- `bar_high >= reference_high`

Low hunt:

- `bar_low <= reference_low`

There is no close requirement.

There is no tolerance.

Equality counts as touch.

## 9. Side mapping

High-side SMT means one symbol hunts a valid reference W high while the other symbol does not. This creates a sell setup on the clean non-hunted symbol.

Low-side SMT means one symbol hunts a valid reference W low while the other symbol does not. This creates a buy setup on the clean non-hunted symbol.

## 10. Confirmation

When SMT divergence forms inside a valid M/W context, the strategy waits until the configured check candle closes.

If at the close of that check candle the divergence is still valid, the signal is confirmed.

If the clean symbol also hunted the same corresponding level before the check candle close, the divergence is invalidated and no entry is allowed.

The close of the same check candle is sufficient. No additional candle is required.

If confirmation would happen on the last check candle ending exactly at the M boundary, no entry is allowed. The signal expires because that time is reserved for partial/hard-close management.

## 11. Check candle construction

Supported check candle periods:

- 1 minute.
- 3 minutes.
- 5 minutes.
- 10 minutes.
- 15 minutes.
- 30 minutes.

All check candles are internally aggregated and anchored from 20:00 New York, the start of the STC trading day.

This means 10-minute candles are 20:00-20:10, 20:10-20:20, and so on. The same anchoring applies to 3m, 5m, 15m, and 30m check candles.

## 12. Entry

Backtest entry model:

- Entry price is the open of the next check candle after confirmation.

Live/paper entry model:

- Market entry immediately after the confirmation check candle closes.

If the EA was offline at the exact entry time, the strategy does not enter later. Delayed entry is not allowed because the stop geometry may no longer be valid.

If Entry STC is OFF at confirmation time, the signal is logged for audit but no trade is opened and no delayed entry is allowed.

## 13. Trade symbol

If Symbol1 hunts and Symbol2 does not, trade Symbol2.

If Symbol2 hunts and Symbol1 does not, trade Symbol1.

The traded symbol is always the clean non-hunted symbol.

## 14. Reference selection for stop

If more than one valid reference W exists for the current W and side, the selected reference is the one that produces the largest stop distance on the clean traded symbol.

This rule replaces earlier smaller-stop ideas. The canonical locked rule is largest stop distance.

The selected reference controls:

- Signal reference identity.
- Stop-loss level.
- Risk distance.
- R-multiple TP calculation.

## 15. Stop loss

For buy trades, SL is placed at the selected reference W low of the traded symbol.

For sell trades, SL is placed at the selected reference W high of the traded symbol.

No buffer is added.

## 16. Take profit

Final Reward is an R-multiple.

Final Reward 10 means TP = 10R from entry.

TP is calculated from raw price distance only. Spread, commission, and slippage do not change the TP price. They are used only for reporting and net performance analysis.

## 17. Trade limit

Each M may open at most three trades total across both symbols.

The counter increments only when a position is actually opened.

If an order fails, the signal is consumed, but the M trade counter is not incremented.

## 18. Hedging

Hedging OFF:

- The first opened trade inside each M locks the direction of that M.
- Direction lock is direction-based, not symbol-based.
- If the first trade in M is buy, only buy trades are allowed until the end of that M.
- If the first trade in M is sell, only sell trades are allowed until the end of that M.
- The lock does not carry into the next M.
- Different M cycles inside the same STC trading day may have opposite directions.

Hedging ON:

- Buy and sell trades may both occur inside the same M.
- The maximum three-trades-per-M rule still applies.
- If buy and sell confirm in the same check candle, no trade is allowed.

## 19. Simultaneous buy and sell

If a buy setup and a sell setup confirm in the same check candle, the strategy discards that check-candle event completely.

No trade is opened.

The ambiguous event is logged as discarded.

The system must not retry that exact ambiguous event later.

## 20. Position management

Open positions are managed continuously, including during gaps.

SL and TP events are valid whenever they occur.

At the end of W4 for M1 and M2, partial close is checked.

At the end of M3, hard close has priority and partial is disabled.

At 15:30 New York, every open STC position must be closed without exception.

If hard close is missed due to EA downtime, it must be executed at the first opportunity after restart, with retry every configured number of seconds until complete.

## 21. Restart recovery

After restart, the EA reconstructs current-day state from:

1. Current STC trading-day candles.
2. Persistent daily journal files.
3. Open positions with this strategy magic number.

It must not rebuild signals from previous STC trading days.

It must not create delayed entries for missed signals.

It may perform delayed partials and delayed hard close if they are still required.

## 22. Drawing

Drawing is required for audit and debugging. Drawing must not ask additional strategy questions. It should show cycles, W reference levels, hunts, divergence candidates, confirmations, rejected reasons, entries, SL, TP, partials, and hard close events.

The drawing layer is observational. It must not affect strategy decisions.
