# Level 08 — Risk Plan and No-Order Paper Entry Model

## Purpose

Level 08 converts the confirmed, consumed signal rows from Level 07 into a deterministic paper entry plan. It still does not send orders, does not modify positions, does not perform partial close, and does not run final outcome simulation. The goal is to prove that every accepted STC signal can be translated into a concrete execution plan with entry price, stop loss, take profit, risk money, theoretical volume, broker volume constraints, and per-M paper trade counters.

This level exists because STC execution must be auditable before live trading. The signal side is already locked: a valid SMT candidate is confirmed only at the close of a check candle, a forgotten same-check buy/sell ambiguity is never carried forward, Entry STC OFF is audit-only, and missed entry moments do not create delayed entries. Level 08 preserves all of those rules and adds the first execution-shaped object: a no-order paper trade plan.

## Locked owner rules implemented in this level

- Paper entry uses the open of the next check candle after confirmation.
- The protective stop is the selected reference W level on the clean traded symbol.
- Final Reward is an R multiple. Final Reward 10 means 10R.
- TP is calculated from raw price distance, without transaction costs.
- Costs are recorded for net reporting only and must not move SL or TP.
- If Entry STC is OFF at confirmation, the signal is recorded but no later entry is allowed.
- If the EA was offline at the exact entry moment, no later entry is allowed.
- If the final check candle of an M confirms a candidate, no entry is allowed.
- If buy and sell appear in the same check candle, that check candle is forgotten.
- Max trades per M is three across Symbol1 and Symbol2 together.
- Hedging OFF locks direction only inside the same M. Different M cycles can have opposite directions.
- Volume has no internal strategy cap, but broker min/max/step must be respected.
- If theoretical volume is above broker max, later auto-trade levels should split orders.
- If theoretical volume is below broker min, Level 08 rejects the paper entry instead of rounding up risk.
- Symbol1 and Symbol2 are both data symbols and execution symbols.
- Level 08 still uses only the magic-owned strategy context and sends no orders.

## Algorithm layer

For each closed check candle that has enough future data to inspect the next check-candle open, Level 08 repeats the same signal-generation path as Levels 05-07:

1. Build the check candle audit row.
2. Ensure the check candle is inside an active M and is detection/entry eligible.
3. Ensure pair data is complete.
4. Load legal previous-W references according to the locked matrix.
5. Detect high and low touch-only hunts with equality as touch.
6. Convert exactly-one-symbol high hunts into Sell candidates on the clean symbol.
7. Convert exactly-one-symbol low hunts into Buy candidates on the clean symbol.
8. If high and low candidates exist in the same check candle, write a forgotten/no-paper row.
9. Select the largest-stop reference for each clean traded symbol.
10. Finalize the candidate into a Level 07-style consumed signal object.
11. Convert only confirmed eligible signals into Level 08 paper entry plans.

## Paper entry construction

A confirmed signal from check candle `N` has paper entry check `N+1`.

The entry price is the open of the trade symbol on the next check candle. The stop is the selected reference price. For a Buy, risk distance is `entry - stop`. For a Sell, risk distance is `stop - entry`. If this distance is not positive, the paper entry is rejected because the selected reference is no longer on the protective side of the next-check open.

TP is then calculated as:

- Buy: `entry + risk_distance * FinalRewardR`
- Sell: `entry - risk_distance * FinalRewardR`

The TP is raw and does not include spread, slippage, or commission. Reporting costs are captured separately.

## Risk and sizing model

The money at risk is:

`equity_snapshot * risk_percent / 100`

If the broker provides a valid `SYMBOL_TRADE_TICK_SIZE` and `SYMBOL_TRADE_TICK_VALUE`, Level 08 uses them:

`money_per_price_unit_per_lot = tick_value / tick_size`

Otherwise it falls back to the shared Contract Size input:

`money_per_price_unit_per_lot = ContractSize`

The theoretical volume is:

`risk_money / (risk_distance_price * money_per_price_unit_per_lot)`

The theoretical volume is not capped by the strategy. Broker min/max/step are still recorded and respected in the paper plan:

- Below broker minimum: reject the paper entry because rounding up would exceed intended risk.
- Above broker maximum: mark as split required; later auto-trade levels may split the order.
- Inside limits: mark as planned.

## Per-M paper counters

Level 08 maintains in-memory paper counters for M1, M2, and M3 separately. A planned paper entry increments the counter for its own M. Rejected or skipped rows do not increment the counter.

If Hedging is OFF, the first planned paper entry inside an M locks that M direction. Opposite signals inside the same M are rejected. The lock does not carry into other M cycles. This implements the owner rule that hedging is scoped to each M only, not to the whole STC day.

The maximum counter value is three per M across both symbols together.

## Output

Level 08 writes:

`stc_level08_paper_entries.csv`

The file contains one row per paper entry decision, including rejections. Important fields include:

- signal id
- paper trade id
- signal check index
- entry check index
- direction
- trade symbol
- hunted symbol
- clean symbol
- selected reference W
- selected reference price
- entry price
- stop price
- take profit price
- risk distance
- reward distance
- equity snapshot
- risk percent
- risk money
- tick value and tick size
- contract size fallback
- theoretical volume
- broker min/max/step
- split order count
- spread points for reporting
- commission for reporting
- M trade count before and after
- M direction lock before and after
- status and rule note

## Level boundary

Level 08 does not decide final trade outcome. It does not check whether SL or TP is hit after entry. It does not perform partial close. It does not run 15:30 hard close. It does not draw objects. It does not send market orders. Those belong to later levels.

The next level should be Level 09: paper outcome simulator and trade journal. It will use Level 08 paper entries and then walk future check candles to classify TARGET, STOP, AMBIGUOUS, PARTIAL_PENDING, HARD_CLOSE, or STILL_OPEN according to the locked rules.
