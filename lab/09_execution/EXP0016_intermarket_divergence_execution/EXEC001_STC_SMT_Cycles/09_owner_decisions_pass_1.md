# 09 - Owner Decisions, Clarification Pass 1

This document records the strategy-owner clarifications that override ambiguity in the source SRS.

## Time gaps

During the gaps between M cycles, the strategy does not open new trades.

No new detection or entry is required during these gaps. Position management remains active only for final TP or other already-open trade management.

The relevant gaps are:

- 02:00 -> 03:00 New York.
- 09:00 -> 09:30 New York.

## W high/low construction

The high and low of each W are the high and low of the synthetic 90-minute W candle.

The timeframe used to derive this high/low is not conceptually important as long as the final W high/low is correct. Internally, the implementation may aggregate from M1 or from the selected available data source.

## W reference matrix

A W never compares with itself.

W1 produces no signal.

W2 can compare only with W1.

W3 can compare only with W2 and W1.

W4 can compare only with W3, W2, and W1.

All comparisons stay inside the same M.

## Hunt rule

Hunt is touch-only.

No tolerance is used.

High hunt uses direct touch of the reference high.

Low hunt uses direct touch of the reference low.

No candle close requirement exists for the raw hunt event.

## Structural comparison

Each symbol has its own W levels.

The comparison is structural, not price-shared.

Example:

- Symbol1 hunts Symbol1 W2 low.
- Symbol2 does not hunt Symbol2 W2 low.
- This is a structural low-side SMT divergence.

## Direction mapping

High-side SMT divergence is a sell setup.

Low-side SMT divergence is a buy setup.

## Trade symbol selection

The trade is placed on the symbol that did not hunt.

If SPX hunts and NDX does not, trade NDX.

If NDX hunts and SPX does not, trade SPX.

The same logic applies to NQ, NAS100, or equivalent broker/index symbols.

## Reference W selection

The reference W is the previous W level used for the stop-loss anchor.

The default selection is the closest eligible reference W in time.

The purpose of the nearest reference is to place a smaller stop.

The implementation may also support an optional test mode that chooses the eligible reference producing the smallest stop distance.

If W4 hunts W3, W2, and W1 references at the same time, W3 is the default reference because it is the closest in time.

## Simultaneous signals

If buy and sell signals are confirmed in the same check candle, no trade is opened.

The simultaneous event is ignored for execution.

If buy and sell occur on separate check candles and hedging is ON, both directions are allowed subject to the M-level max-trade limit.

## Confirmation

After raw divergence forms, the EA waits for the active check candle to close.

If the divergence is still valid at check-candle close, entry occurs immediately.

If the clean symbol hunts before the check candle closes, the divergence is invalidated and no trade is opened.

The close of the same active check candle is sufficient. A new full candle is not required.

Each valid signal can produce only one entry. If the same divergence remains valid on later check candles, no additional entries are opened.

The final check candle of an M is not used for new entry. That time is reserved for partial-close logic, and at 15:30 New York it is reserved for full daily close/reset.

## M-level trade counter

The max-trade counter is per M across both symbols combined.

For M1, SPX and NDX together can open at most three trades.

The counter increases only when a position is actually opened.

## Hedging

When hedging is OFF, direction lock is based only on direction, not symbol.

If the first trade in an M is buy, only buy trades are allowed until the end of that M.

If the first trade in an M is sell, only sell trades are allowed until the end of that M.

When hedging is ON, both buy and sell trades may occur in the same M, subject to max three trades per M.

Even when hedging is ON, if buy and sell are confirmed in the same check candle, no trade is opened.

## Spread

The strategy does not filter entries based on spread.

Spread and commission should still be recorded in reports and optionally included in net performance analysis.

## Stop-loss

The stop-loss is based on the selected reference W of the trade symbol.

If SPX hunts and NDX is the clean/traded symbol, the SL is placed on the NDX reference W, not the SPX reference W.

No buffer is added.

## Final Reward and TP

Final Reward is an R multiple.

Final Reward = 10 means a 10R take profit.

If risk distance is 20 points, the TP distance is 200 points.

## Position sizing

Use broker tick value if available.

If tick value is not available, use the Contract Size input, default 10.

Risk sizing remains important, but the exact source of tick value vs contract size is not strategically critical.

The EA does not impose its own theoretical maximum volume cap. However, live orders must still respect broker minimum, maximum, and volume-step constraints because the broker will enforce them.

## Partial close

Partial close times are the end of W4 for each M:

- M1 partial check: 02:00 New York.
- M2 partial check: 09:00 New York.
- M3 partial check: 15:30 New York.

At the end of M3, partial close is effectively irrelevant because the daily hard close occurs at 15:30.

Partial close occurs even if the trade is currently in loss, as long as it has not reached TP.

Partial volume is rounded upward to the broker volume step.

A trade opened in M1 is not partially closed again in M2.

Each trade can be partially closed at most once.

## Daily hard close

After 15:30 New York, no STC trade from that trading day may remain open.

All open positions managed by this strategy are closed at 15:30 New York.

All day state is reset after the close.

## Current-day data scope

Previous-day data must not influence the current trading day's decisions.

After reset, previous-day W levels, divergences, counters, and partial states are not retained for decision-making.

If the EA restarts during the same trading day, it may rebuild current-day state from current-day data and may detect open positions from the account.

## Entry OFF behavior

When STC Entry is OFF, the strategy still scans and records events for audit/reporting, but it does not open new trades.

Position management for previously opened trades continues.

## Instance behavior

The EA can be attached to either of the two configured index charts.

The chart symbol does not change the logic.

## Check-candle construction

The EA should internally aggregate check candles so that non-standard intervals such as 3m and 10m are supported consistently.

## Entry price for backtest

The preferred research/backtest entry model is next-bar open after the check-candle close.

## Backtest path

The backtest may use the same check candle path for SL/TP checks at this stage.

## Costs

Spread and commission should be added to the reporting model.

## Missing data / holidays

If data is missing or the market is closed, no trade is opened.

## Symbol families

The same strategy logic applies to SPX/NDX, ES/NQ, US500/NAS100, or equivalent broker symbols.
