# 14 - Backtest and Live Runtime

## 1. Runtime modes

The implementation should support three modes:

1. Research backtest.
2. Paper live.
3. Auto trade.

The first build should prioritize research backtest and paper live. Auto trade should be enabled only after deterministic tests pass.

## 2. Research backtest runtime

Backtest loop:

1. Load Symbol1 and Symbol2 bars.
2. Convert timestamps to New York time.
3. Build STC trading days.
4. For each day, build M/W structure.
5. Build check candles anchored at 20:00.
6. Process completed check candles in chronological order.
7. Detect and confirm SMT.
8. Create simulated entries at next check-candle open.
9. Simulate SL/TP/ambiguous outcomes using check-candle bars.
10. Apply partial and hard close rules.
11. Write journals and summary.

## 3. Backtest data requirements

Both symbols must have complete data for signal decisions.

If either symbol is missing data for a required W or check candle, no trade is allowed for that decision point.

Missing data must be logged.

## 4. Backtest entry timing

If signal confirms at check candle close T, entry is at the open of the next check candle.

If the next check candle would start outside the same M or at the M boundary, no entry is allowed.

## 5. Backtest outcome timing

Outcome is evaluated using the configured check-candle timeframe.

If an open trade's next check candle touches TP only, outcome is TP.

If it touches SL only, outcome is SL.

If it touches both TP and SL, outcome is AMBIGUOUS.

If neither is touched, the trade remains open until partial, hard close, TP, SL, or ambiguous outcome.

## 6. Paper live runtime

Paper live loop:

1. OnTimer runs every configured seconds.
2. Convert current time to NY.
3. Load/update bars for both symbols.
4. If a new check candle closed, run signal logic.
5. If signal confirms, write paper trade instead of real order.
6. Manage paper position outcomes.
7. Draw updates.
8. Write journals.

Paper live must not enter delayed missed signals.

## 7. Auto-trade runtime

Auto-trade loop is the same as paper live, except confirmed trade intents send real broker orders.

Auto-trade must:

- Respect broker min/max/step.
- Split orders above broker maximum.
- Skip below broker minimum.
- Use only strategy magic number.
- Retry hard close until complete.
- Write every order send and close attempt.

## 8. Live entry failure

If an order fails:

- Signal is consumed.
- M trade counter is not incremented.
- No retry in later candles.
- Journal records the broker error.

## 9. Offline-at-entry behavior

If the EA was offline when a signal should have entered, it must not enter after restart.

Reason: the entry is no longer at the intended check-candle boundary and stop geometry may no longer be valid.

The event can be reconstructed and logged as `EA_OFFLINE_AT_ENTRY_NO_DELAYED_ENTRY`.

## 10. Delayed actions allowed

Delayed entry is forbidden.

Delayed partial is allowed and required.

Delayed hard close is allowed and required.

This distinction is central:

- Entries are timing-sensitive.
- Position management is obligation-sensitive.

## 11. Runtime safety rules

The EA must:

1. Use duplicate instance lock.
2. Manage only magic-number positions.
3. Never use previous STC day data for signals.
4. Never enter in gaps.
5. Never enter on final check candle of M.
6. Continue position management in gaps.
7. Retry hard close until complete.
8. Write enough audit data to explain every decision.
