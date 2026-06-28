# 10 - Owner Decisions, Clarification Pass 2

This document records the second owner clarification pass. These decisions supersede any earlier unresolved implementation questions.

## Exact touch operator

Exact equality counts as touch.

- High hunt: `high >= reference_high`.
- Low hunt: `low <= reference_low`.

No tolerance or buffer is applied.

## Gap handling

No new detection and no new entry occur during the gaps between M cycles.

Position management remains active for already-open trades. If SL or TP is reached during a gap, the open position is managed normally. After an SL or TP event in a gap, the strategy waits until the next eligible M/check-candle context for any future entry decision.

## Delayed partial close

Partial close is scheduled exactly at the end of W4 for M1 and M2.

If the EA is offline or unable to process the scheduled partial close at the exact time, it must execute the missed partial close at the first later opportunity, as long as:

- the position is still open;
- the position belongs to the M whose partial event was missed;
- the position has not already been partially closed;
- the current STC trading day has not been hard-reset.

The missed partial is executed even if the EA has already moved into a later M.

## M3 end behavior

At the end of M3, partial close may be disabled because the 15:30 New York hard close takes priority.

If the hard close is missed because the EA was offline, the hard close must be executed at the first later opportunity. No STC position from that trading day may remain open after 15:30 New York.

## Backtest entry price

Research/backtest entry price uses the next check-candle open after the confirmation candle closes.

Live entry uses market execution immediately after the confirmation candle closes.

## Check-candle anchoring

All internally aggregated check candles are anchored from the STC trading-day start at 20:00 New York.

Examples:

- 10-minute check candles begin at 20:00, 20:10, 20:20, etc.
- 3-minute check candles begin at 20:00, 20:03, 20:06, etc.

This makes all check-candle partitions deterministic and independent of chart timeframe.

## Final check candle of an M

If a check candle closes at or after the end of the current M, no new entry is allowed from that check candle.

The final check candle of each M is reserved for M-end management such as partial processing or the 15:30 hard close.

## Reference selection changed to largest stop

When multiple eligible previous W references exist for the same side and same clean/traded symbol, the selected reference is the one that produces the largest stop distance for the clean/traded symbol.

This replaces the earlier closest-by-time default.

The purpose of this rule is to choose the safer/wider stop anchor when multiple references are simultaneously valid.

## Multiple references in the same check candle

If several eligible references produce the same-side divergence for the same trade symbol in the same check candle, they are treated as one signal. The reference that creates the largest stop distance for the clean/traded symbol is selected.

The implementation should not open multiple trades only because several previous W references were valid at the same time.

## Multiple same-direction signals

Within one check candle, if multiple same-direction candidates exist, the engine should resolve them into the logically strongest executable signal per trade symbol using the selected-reference rule.

If more than one clean trade symbol is still executable in the same check candle, the implementation may open multiple trades as long as:

- all signals are same-direction;
- hedging/direction-lock rules allow the direction;
- the M-level maximum of three opened trades is not exceeded;
- each signal has a unique divergence identity.

The audit journal must record the resolution order and the reason each candidate was executed or skipped.

## Simultaneous buy and sell

If buy and sell signals are confirmed in the same check candle, the entire check-candle signal set is ignored for execution.

The simultaneous buy/sell event is forgotten for trade execution. It does not generate delayed entry later.

## Entry OFF behavior

If STC Entry is OFF at the exact time a signal would normally enter, no trade is opened.

The signal is recorded for audit only.

The strategy must not enter the same signal later if Entry STC is turned back ON after the original entry time has passed.

## EA offline at entry time

If the EA is offline at the exact time a trade should have been entered, the trade is not entered later.

The reason is that the stop quality may no longer be valid after the intended entry time.

## Order failure

If a signal confirms and an order attempt is made but no position is opened, the signal is consumed for trading and must not be retried on later check candles.

The M trade counter increases only when a position is actually opened.

## Hedging scope

Hedging applies only inside each M.

If hedging is OFF, the first opened trade in an M locks the allowed direction for that M only.

Different M cycles in the same STC trading day may contain opposite-direction positions/signals when allowed by their own M-level state.

## M trade limit

Each M allows at most three opened trades across both configured symbols combined.

The limit is an opened-position limit, not a signal-count limit.

## Broker volume limit handling

The strategy does not impose its own theoretical max-volume cap.

For live execution, if the required volume exceeds broker maximum volume, the EA may split the order into multiple valid broker-sized orders until the requested theoretical volume is reached or the M/trade safety rules prevent further execution.

If the required volume is below broker minimum volume, the trade should be skipped unless a future explicit input enables minimum-volume execution.

## Contract size

Contract Size remains a single shared input for both configured symbols when broker tick value is unavailable.

If broker tick value is available, broker tick value is preferred.

## TP and cost treatment

Final Reward remains an R multiple.

TP is calculated from raw entry-to-SL price distance.

Spread, commission, and slippage do not change the TP placement. Costs are used for reporting and net-performance analysis.

## Spread and commission source

Spread should be read from market/broker data when available.

Commission should be read from broker/deal data when available. If broker-side commission is unavailable in research mode, a reporting input may be used.

## SL/TP ambiguity in a single backtest candle

If one backtest candle touches both SL and TP and the lower-timeframe sequence is unknown, the event must be reported as ambiguous.

Do not force SL-first or TP-first for the locked specification.

The trade journal should preserve this as an explicit ambiguous outcome category.

## SL/TP checking candle

Backtest outcome is checked using the same check-candle series at this stage.

## Missing data

Both symbols must have complete enough data for the relevant cycle/check window.

If either symbol is missing data or the market is closed, the pair is not tradable for that event.

Incomplete data invalidates the candidate for trading and must be recorded in audit.

## Restart and persistence

The EA must reconstruct current-day state from:

- current STC trading-day candles;
- persistent daily journal/state files;
- currently open account positions that belong to the strategy magic number.

This prevents duplicate entries after restart and preserves partial/consumed-signal state.

## Instance lock

The implementation must prevent duplicate execution when the EA is attached to multiple charts.

Use a global lock keyed by strategy id and symbol pair.

Only one active executable instance is allowed for the same strategy-symbol pair.

## Symbol model

For this STC strategy, the two configured symbols are the data symbols and the execution symbols.

No separate CME-data-to-broker-execution mapping is part of this strategy version.

The same logic applies to SPX/NDX, ES/NQ, US500/NAS100, or equivalent index/futures broker symbols.

## Drawing

Drawing is required for audit and visual inspection.

The implementation owner delegates the drawing design to the developer. The drawing layer should include, at minimum:

- M and W cycle boxes/regions;
- reference W high/low levels;
- hunt markers;
- confirmed divergence markers;
- entry, SL, TP lines;
- partial-close markers;
- daily reset/hard-close markers.

No additional owner clarification is required for drawing unless it affects strategy logic.

## Output journals

The implementation should produce whatever audit outputs are necessary for verification. Required baseline outputs are:

- cycle audit;
- divergence audit;
- trade journal;
- state/restart audit;
- drawing/debug summary when chart rendering is enabled.

## Implementation modes

The preferred implementation sequence is:

1. Research mode.
2. Paper/live-monitor mode.
3. Auto-trade mode.

## Hard-close retry

If the hard close cannot be completed at 15:30 New York, the EA retries every few seconds until all strategy-managed positions are closed.

Hard close is always active and is not disabled by Entry STC OFF.

## Position ownership

The EA manages only positions created with its own magic number.

Manual trades or trades from other strategies are not managed.

## STC trading-day boundary

The term "previous day" means any data before the current STC trading-day start, not necessarily calendar midnight.

Current-day state begins at the STC trading-day start of 20:00 New York.
