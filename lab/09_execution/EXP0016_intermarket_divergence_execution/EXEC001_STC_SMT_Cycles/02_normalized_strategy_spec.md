# 02 - Normalized Strategy Specification

## Strategy identity

Name: STC SMT Cycles

Family: Intermarket divergence execution

Strategy code: EXEC001_STC_SMT_CYCLES

Source: STC Expert Advisor SRS v1.0 plus owner clarification pass 1.

## Purpose

The strategy trades SMT divergence between two configured index symbols using only the current STC trading day.

The EA may be attached to any chart, but the chart symbol must not influence decisions. The two configured symbols are the only symbols analyzed and managed.

## Canonical trading day

Timezone: New York.

Trading day start: 20:00 New York.

Trading day end: 15:30 New York on the following calendar day.

At 15:30 New York:

- all strategy-managed positions are closed;
- all M counters are reset;
- all divergence records are cleared;
- all partial-close state is cleared;
- all entry-consumption state is cleared;
- previous-day information is no longer available for decision-making.

The EA may rebuild current-day state after restart using only current-day data.

## M cycles

M1: 20:00 -> 02:00 New York.

Gap: 02:00 -> 03:00 New York. No new entry and no new detection is required.

M2: 03:00 -> 09:00 New York.

Gap: 09:00 -> 09:30 New York. No new entry and no new detection is required.

M3: 09:30 -> 15:30 New York.

## W cycles

Each M has four W cycles. Each W is a synthetic 90-minute candle.

M1:

- W1: 20:00 -> 21:30
- W2: 21:30 -> 23:00
- W3: 23:00 -> 00:30
- W4: 00:30 -> 02:00

M2:

- W1: 03:00 -> 04:30
- W2: 04:30 -> 06:00
- W3: 06:00 -> 07:30
- W4: 07:30 -> 09:00

M3:

- W1: 09:30 -> 11:00
- W2: 11:00 -> 12:30
- W3: 12:30 -> 14:00
- W4: 14:00 -> 15:30

## W high/low construction

The W high and W low are the high and low of the synthetic 90-minute W candle.

The construction timeframe is not strategically meaningful as long as the final W high and low are correct.

The implementation may aggregate W values from M1 or another available data source.

## Reference matrix

Current W never compares with itself.

W1 never generates signals.

W2 compares only with W1.

W3 compares only with W2 and W1.

W4 compares only with W3, W2, and W1.

All references must be inside the same M.

## SMT divergence definition

A valid SMT divergence occurs when exactly one symbol hunts a previous eligible W high or W low while the other symbol does not hunt its corresponding same-structure W level.

The comparison is structural. Each symbol has its own W levels.

High-side divergence:

- one symbol touches an eligible previous W high;
- the other symbol does not touch its corresponding eligible previous W high;
- setup direction is sell;
- trade is placed on the clean symbol.

Low-side divergence:

- one symbol touches an eligible previous W low;
- the other symbol does not touch its corresponding eligible previous W low;
- setup direction is buy;
- trade is placed on the clean symbol.

## Hunt rule

Hunt is touch-only.

No candle close beyond the level is required.

No tolerance is used.

High hunt: current high touches the reference high.

Low hunt: current low touches the reference low.

## Check-candle confirmation

The strategy waits for the active check candle to close after raw divergence appears.

If the divergence still exists at that check-candle close, entry occurs immediately.

If the clean symbol has also hunted the corresponding reference before the check candle closes, the divergence is invalid and no trade is opened.

The same active check candle is sufficient. The strategy does not require a full new check candle after formation.

Allowed check-candle sizes:

- 1m
- 3m
- 5m
- 10m
- 15m
- 30m

The EA should aggregate check candles internally so non-native periods such as 3m and 10m remain supported.

## Last-check-candle rule

The final check candle of an M is not used for new entries.

The end of W4 is reserved for partial close, and at 15:30 New York it is reserved for daily hard close.

If confirmation would occur only after the M has ended, the signal is cancelled.

## One-entry-per-divergence

Each divergence can open at most one trade.

If the same divergence remains valid in later check candles, no additional entries are opened.

## Simultaneous signal rule

If buy and sell signals are confirmed in the same check candle, no trade is opened.

If buy and sell signals occur in separate check candles and hedging is ON, both directions are allowed subject to the max-trade limit.

## Max trades per M

Each M can open at most three trades total across both symbols.

The counter increases only after a position is actually opened.

## Hedging

If hedging is OFF, the first opened trade in an M locks the allowed direction for that M.

The lock is direction-based and not symbol-based.

If hedging is ON, both buy and sell trades are allowed, but the max three trades per M still applies.

Even with hedging ON, simultaneous buy and sell confirmation in the same check candle produces no trade.

## Stop-loss

SL is placed exactly on the selected reference W high or low of the trade symbol.

No buffer is added.

For buy trades, SL uses the selected reference W low of the trade symbol.

For sell trades, SL uses the selected reference W high of the trade symbol.

When multiple eligible reference W levels are involved, the default reference selection is the closest eligible W by time. An optional research mode may choose the eligible reference that produces the smallest stop distance.

## Take-profit

All trades have TP.

TP is based on Final Reward as an R multiple.

Final Reward = 10 means 10R.

## Position sizing

Position size is calculated from Equity and Risk Percent.

If broker tick value is available, use broker tick value.

If tick value is not available, use Contract Size input.

The strategy does not apply its own theoretical max-volume cap, but live execution must respect broker min/max/step constraints.

## Partial close

If Partial is OFF, no partial close is performed.

If Partial is ON, at the end of W4 of each M, trades opened in that same M are checked.

If a trade has not reached TP, approximately 50% of the volume is closed.

Partial volume is rounded upward to broker volume step.

If the trade volume is 0.01 and a valid smaller partial is not possible, the full position is closed.

Each trade can be partially closed only once.

Trades opened in M1 are not partially closed again in M2.

At M3 end, partial is practically superseded by the daily hard close.

## STC Entry OFF

When STC Entry is OFF:

- no new trades are opened;
- signals and events may still be recorded for audit;
- management of already-open positions continues.

## Missing data

If required data is missing or the market is closed, no trade is opened.

## Costs

Spread and commission should be recorded and included in net reports.

The strategy does not use spread as an entry filter.
