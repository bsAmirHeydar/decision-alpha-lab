# 04 - SMT Divergence Rules and Algorithms

## 1. Scope

SMT divergence is defined only between Symbol1 and Symbol2.

The strategy compares each symbol against its own W-cycle reference levels. It never compares one symbol's absolute price level to the other symbol's absolute price level.

## 2. Reference eligibility

Inside each M:

- W1 has no eligible references and cannot signal.
- W2 references W1.
- W3 references W2 and W1.
- W4 references W3, W2, and W1.

The current W never references itself.

No W may reference a W from another M.

No W may reference a W from a previous STC trading day.

## 3. Reference records

For each symbol, each completed W produces:

- W ID.
- Symbol.
- M ID.
- Start time.
- End time.
- High.
- Low.
- Data completeness status.

The reference levels used by the current W are the completed previous W records inside the same M.

## 4. Hunt definition

High hunt occurs when the active check candle high is greater than or equal to the selected symbol's reference W high.

Low hunt occurs when the active check candle low is less than or equal to the selected symbol's reference W low.

Equality counts as touch.

No tolerance is used.

No close condition is required.

## 5. Candidate detection

At every active check-candle update inside a non-final check candle:

1. Determine current M and W.
2. If current W is W1, stop; no signal is possible.
3. Load eligible references for current W.
4. For each reference candidate and side, evaluate Symbol1 hunt status and Symbol2 hunt status.
5. If both symbols hunted, no SMT exists for that reference.
6. If neither symbol hunted, no SMT exists for that reference.
7. If exactly one symbol hunted, create an SMT candidate.

## 6. Side mapping

High reference hunted by exactly one symbol:

- Setup side: SELL.
- Hunted symbol: the symbol that touched its own reference high.
- Clean symbol: the symbol that did not touch its own reference high.
- Trade symbol: clean symbol.
- Stop reference: selected reference high of trade symbol.

Low reference hunted by exactly one symbol:

- Setup side: BUY.
- Hunted symbol: the symbol that touched its own reference low.
- Clean symbol: the symbol that did not touch its own reference low.
- Trade symbol: clean symbol.
- Stop reference: selected reference low of trade symbol.

## 7. Multiple reference resolution

If multiple eligible references create valid SMT candidates for the same clean symbol and side, the strategy selects the reference that produces the largest stop distance on the clean traded symbol.

For buy:

- Stop distance = entry price candidate - reference low of clean symbol.

For sell:

- Stop distance = reference high of clean symbol - entry price candidate.

Because the final entry price is known only after confirmation, the selection engine must use the best available confirmation-time or projected entry price. In backtest, the exact next-check-candle open is available after confirmation. In live, selection uses the market price immediately after confirmation.

The selected reference becomes the signal reference. Other references are audit-only for that event.

## 8. Confirmation rule

A candidate is not tradable immediately when it first forms.

The engine waits until the active check candle closes.

At close, it re-evaluates the candidate:

- The hunted symbol must still have hunted.
- The clean symbol must still not have hunted.
- The current check candle must not be the final check candle of the M.
- Data for both symbols must be complete.
- The M trade limit must not be exhausted.
- Direction lock must allow the side if Hedging is OFF.
- Entry STC must be ON for live execution, or the signal is audit-only.

If all checks pass, the signal is confirmed.

## 9. Candidate invalidation before confirmation

A candidate becomes invalid if before confirmation close:

- The clean symbol also hunts the corresponding reference.
- Data becomes incomplete.
- Time moves into a gap or beyond the M end.
- Buy and sell ambiguity appears in the same check candle.

Invalidated candidates are logged for audit.

## 10. Simultaneous buy and sell

If a buy signal and a sell signal confirm inside the same check candle, the engine discards the entire check-candle trade decision.

No trade is opened.

The event is logged as `AMBIGUOUS_BUY_SELL_DISCARDED`.

The discarded event is not eligible for delayed entry or retry.

## 11. Same-direction multiple signals

If multiple same-direction unique signals confirm in the same check candle, the engine may open multiple trades until the maximum three trades per M is reached.

However, for the same clean symbol and same side inside the same check candle, only one trade is allowed. The reference-selection rule chooses the largest-stop reference.

A deterministic ordering must be used when more eligible trades exist than remaining M capacity. Recommended ordering:

1. Largest stop-distance reference first.
2. Earliest formation time second.
3. Symbol1 before Symbol2 as final tie-breaker.

## 12. Signal identity

A signal identity should include:

- STC trading-day ID.
- Strategy ID.
- M ID.
- Current W ID.
- Check-candle close time.
- Side.
- Hunted symbol.
- Clean/trade symbol.
- Selected reference W ID.
- Reference side high/low.

This identity prevents duplicate entries after restart.

## 13. Consumed signals

A signal is consumed when:

- It successfully opens a position.
- Entry STC is OFF at confirmation time.
- The EA was offline at the exact entry time and the opportunity is reconstructed later.
- Order send fails.
- It is rejected by direction lock.
- It is discarded because buy and sell confirmed in the same check candle.

Consumed signals must not be entered later.

## 14. Algorithm: detect and confirm SMT

1. On every completed check candle, determine cycle context.
2. If outside M or inside gap, skip detection.
3. If check candle is final for the M, skip entry and mark final-window candidates as expired.
4. Build current W and eligible previous W references.
5. Skip if current W is W1.
6. Evaluate high and low hunts for both symbols against all eligible references.
7. Build candidate list for exactly-one-symbol-hunted cases.
8. Resolve multiple references by largest stop distance on the clean traded symbol.
9. Remove ambiguous buy/sell same-check-candle events.
10. Apply Entry ON/OFF, trade counter, direction lock, data completeness, and duplicate-signal filters.
11. Confirm tradable signals.
12. Send to execution simulator/live executor.
13. Write all accepted and rejected candidates to audit logs.
