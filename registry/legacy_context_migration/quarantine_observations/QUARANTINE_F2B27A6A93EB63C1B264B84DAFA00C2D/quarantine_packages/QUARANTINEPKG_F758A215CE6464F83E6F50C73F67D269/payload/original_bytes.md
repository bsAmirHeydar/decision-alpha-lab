# 05 - Execution, Risk, Position Management, and Outcomes

## 1. Entry model

Backtest:

- The strategy confirms at the close of a check candle.
- Entry price is the open of the next check candle.
- If there is no next check candle inside the same M, no entry is allowed.

Live/paper:

- Entry is a market order immediately after the confirmation check candle closes.
- If the EA is offline at the exact entry time, no delayed entry is allowed.

## 2. Entry STC switch

If Entry STC is ON, confirmed signals may execute.

If Entry STC is OFF:

- The signal is audited.
- No trade is opened.
- The signal is consumed for trading.
- The strategy must not enter later if Entry STC is turned ON.
- Existing positions continue to be managed.

## 3. Trade symbol

The trade is always opened on the clean symbol that did not hunt.

The strategy uses `Symbol1` and `Symbol2` as both signal symbols and execution symbols.

## 4. Stop loss

Buy trade:

- Stop loss is the selected reference W low of the trade symbol.

Sell trade:

- Stop loss is the selected reference W high of the trade symbol.

No buffer is applied.

## 5. Target

Final Reward is an R-multiple.

If Final Reward = 10, TP = 10R.

Buy TP:

- Entry + FinalReward * abs(Entry - SL).

Sell TP:

- Entry - FinalReward * abs(Entry - SL).

Transaction costs do not change the TP level.

## 6. Risk sizing

Risk money:

- Equity * RiskPercent / 100.

If broker tick value and tick size are available, the engine should use them.

If tick value is unavailable, use the shared Contract Size input. The default fallback Contract Size is 10.

The fallback formula is:

- Volume = RiskMoney / (StopDistancePoints * ContractSize).

The system should report all intermediate values:

- Equity.
- Risk percent.
- Risk money.
- Entry.
- SL.
- Stop distance points.
- Tick value source.
- Contract size fallback.
- Calculated theoretical volume.
- Broker-normalized volume.

## 7. Broker volume limits

The strategy has no internal maximum volume limit.

However, live trading must respect broker min, max, and step constraints.

If calculated volume is greater than broker max, the executor may split the order into multiple broker-valid orders until the target volume is reached or broker constraints prevent more orders.

If calculated volume is below broker minimum, the trade should be skipped rather than increasing risk by forcing minimum volume. This skip must be logged as `VOLUME_BELOW_BROKER_MIN`.

## 8. Order failure

If order send fails:

- The signal is consumed.
- No delayed entry is allowed.
- The M trade counter is not incremented.
- The failure reason is written to the trade journal.

## 9. Trade counter

Each M allows at most three opened trades total across both symbols.

The counter increments only after a position is successfully opened.

The counter does not decrement after stop, TP, partial, or manual closure.

## 10. Hedging OFF

When Hedging is OFF, the first successfully opened trade inside an M locks that M direction.

The direction lock is not symbol-specific.

If the first trade in M is buy, only buy trades are allowed until the end of that M.

If the first trade in M is sell, only sell trades are allowed until the end of that M.

At the next M, direction lock resets. Opposite direction trades are allowed in later M cycles even during the same STC trading day.

## 11. Hedging ON

When Hedging is ON, both buy and sell trades may occur inside the same M, subject to the maximum three trades per M rule.

If buy and sell confirm in the same check candle, no trade is opened even when Hedging is ON.

## 12. Partial close

Partial close applies only if Partial is ON.

Partial is evaluated at the end of W4 for M1 and M2.

M3 partial is disabled because the 15:30 hard close has priority.

At partial time, all positions opened in that same M are checked.

If a position has not reached TP and has not already been partially closed, close approximately 50% of volume.

Rounding rule:

- Partial volume is rounded upward to broker volume step.
- If volume is 1.01 and step is 0.01, partial close volume is 0.51.
- If volume is 0.01, the whole position is closed.

Partial occurs even if the position is in loss.

If partial was missed due to EA downtime, it must be performed later at the first opportunity, regardless of whether the system has moved into a later M, as long as the position is still open and has not already been partially closed.

Each trade can be partially closed only once.

## 13. Hard close

At 15:30 New York, every open STC position must be closed.

Hard close overrides partial.

If hard close is missed because the EA was offline or order close failed, the EA enters hard-close recovery and retries every configured number of seconds until all magic-number STC positions are closed.

Hard close applies even if Entry STC is OFF.

Hard close applies only to positions with this strategy's magic number.

## 14. Gaps and position management

During gaps, no new signal or entry can occur.

Open positions continue to be managed. If SL or TP is hit during a gap, the result is valid.

The backtest engine must include gap candles for outcome if a position is open.

## 15. Stop and TP outcome with check candles

Backtest outcome is evaluated using the configured check-candle timeframe.

If the same check candle after entry touches both SL and TP, the outcome is marked `AMBIGUOUS` rather than guessing the path.

Ambiguous outcomes are not forced into win or loss. Reports must keep them separate.

## 16. Transaction costs

Spread, commission, and slippage are not used to change entry, SL, or TP levels in the canonical strategy logic.

They are used for reporting net performance.

Preferred source:

- Read spread and commission from broker/data when available.
- If unavailable, use report inputs.

Reports must include both gross and net fields.

## 17. Position ownership

The EA manages only positions with its own magic number.

Manual trades and positions from other strategies are ignored unless a future explicit setting changes this behavior.

## 18. Runtime modes

Research mode:

- No real orders.
- Full signal, trade simulation, outcome, drawing, and CSV reports.

Paper mode:

- Live data.
- No real orders.
- Signals are recorded as if executable.

Auto-trade mode:

- Live data.
- Real orders.
- Broker constraints enforced.
- Hard-close recovery always enabled.

The first implementation should prioritize Research and Paper before Auto-trade.
