# 05 - Execution, Risk, TP, Partial, and Reset

## Inputs

Strategy inputs from the SRS and clarification pass:

- Symbol1, default SPXUSD.
- Symbol2, default NDXUSD.
- Entry STC, default ON.
- Partial, default ON.
- Hedging, default OFF.
- Final Reward, default 10.
- Risk Percent, user-defined.
- Candle Check: 1m, 3m, 5m, 10m, 15m, 30m.
- Contract Size, default 10.
- Broker UTC Offset, user-defined.
- Spread/commission reporting inputs or broker-derived cost fields.

## Entry trigger

Entry occurs immediately after the check candle closes and the divergence is still valid.

For research/backtest, the entry price is the open of the next check candle after the confirmation candle closes.

For live trading, entry is a market order immediately after check-candle close.

Each signal opens at most one trade.

If STC Entry is OFF, events may still be recorded, but no new trade is opened.

## Trade symbol

The trade is placed on the symbol that did not hunt.

High-side divergence creates a sell trade on the clean symbol.

Low-side divergence creates a buy trade on the clean symbol.

No alternate symbol is used if the clean symbol is unavailable. If required data is missing or the market is closed, no trade is opened.

Spread is not used as an entry filter.

## M trade limit

Each M allows at most three opened positions across both configured symbols combined.

The counter increases only after a position is successfully opened.

## Hedging OFF

When hedging is OFF, the first opened trade in an M locks the M direction.

If first trade is buy, only buy trades are allowed until that M ends.

If first trade is sell, only sell trades are allowed until that M ends.

Direction lock does not depend on symbol.

## Hedging ON

When hedging is ON, buy and sell trades can both occur in the same M, subject to the max three trades per M.

However, if buy and sell are confirmed in the same check candle, no trade is opened.

## Stop-loss

For buy trades, SL is placed exactly at the selected reference W low of the trade symbol.

For sell trades, SL is placed exactly at the selected reference W high of the trade symbol.

No buffer is added.

If Symbol1 hunts and Symbol2 is traded, the stop is based on Symbol2's selected reference W.

## Reference selection for SL

Default mode:

- closest eligible reference W by time.

Optional research mode:

- eligible reference producing smallest stop distance.

Reports must state which mode was used.

## Take-profit

Final Reward is an R multiple.

Final Reward = 10 means TP = 10R.

Buy TP:

- entry + FinalReward * risk_distance.

Sell TP:

- entry - FinalReward * risk_distance.

TP is not modified after the trade opens.

## Position sizing

Risk money:

- equity * risk_percent / 100.

Use broker tick value if available.

If tick value is unavailable, use Contract Size input.

The strategy does not impose its own theoretical volume cap.

Live execution must still respect broker min volume, max volume, and volume step.

If broker normalization changes the live volume, the report should record both theoretical volume and executed volume.

## Costs

Spread and commission should be recorded.

Reports should support both raw and net performance.

The strategy does not skip trades due to spread.

## Partial close

If Partial is OFF, no partial-close operation occurs.

If Partial is ON, at the end of W4 of each M, the EA checks trades opened in that M.

If a trade has not reached TP, close approximately 50% of the position.

Partial close applies even if the trade is in loss.

Partial volume is rounded upward to the broker volume step.

Example:

- volume 1.01 -> close 0.51 if step is 0.01.
- volume 0.01 -> close the full trade if no smaller valid partial exists.

Each trade can be partially closed only once.

A trade opened in M1 cannot be partially closed again in M2.

At the end of M3, partial close is effectively irrelevant because daily hard close occurs at 15:30.

## Daily hard close

At 15:30 New York, all open positions managed by STC are closed without exception.

After closing positions, all state is reset.

After 15:30 New York, no position from that STC trading day should remain open.

If the EA restarts after 15:30 and detects old STC-managed positions, it should close them for safety.

## Restart behavior

If the EA restarts during the current trading day, it may rebuild state from current-day data only.

It may also inspect account positions to recover active STC-managed positions.

Previous-day signals, W levels, divergence states, and counters must not influence new decisions.

## Clarification pass 2 execution locks

### Offline at entry time

If the EA is offline or unable to enter at the exact intended entry time, the signal is not entered later.

### Entry OFF

If STC Entry is OFF at the intended entry time, the signal is recorded for audit but no trade is opened and no delayed entry is allowed.

### Order failure

If an order attempt fails and no position is opened, the signal is consumed for trading. The M trade counter is not increased.

### Volume handling

The strategy has no theoretical max-volume cap.

Live execution must respect broker min/max/step constraints.

If requested volume is above broker maximum, the EA may split the requested volume into multiple broker-valid orders.

If requested volume is below broker minimum, the trade is skipped unless a future explicit input enables minimum-volume execution.

### Position ownership

Only positions created with the strategy magic number are managed.

Manual trades and other strategy trades are ignored.

### Costs

TP and SL placement are calculated without transaction costs.

Spread, commission, and slippage are used for reporting/net-performance analysis. Spread and commission should be read from broker data when available.

### Ambiguous SL/TP

If the same backtest candle touches both SL and TP and no lower-timeframe sequence is available, the result is recorded as AMBIGUOUS rather than forced to SL-first or TP-first.

### Hard close retry

If 15:30 New York hard close fails or is missed, the EA retries every few seconds until all strategy-owned positions are closed.
