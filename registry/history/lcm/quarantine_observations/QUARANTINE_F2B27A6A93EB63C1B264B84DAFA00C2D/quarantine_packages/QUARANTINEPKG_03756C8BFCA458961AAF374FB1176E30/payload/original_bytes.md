# Level 06 — SMT Candidate Engine

Status: implemented as an audit-only layer.

Level 06 converts the raw hunt material from Level 05 into explicit SMT candidate rows. It still does not confirm signals, consume signals, simulate entries, open positions, draw objects, or manage trades. The output of this level is a deterministic candidate audit table that later levels can use for confirmation, signal registry, paper execution, and auto-trading.

## Scope

Level 06 is responsible for these operations:

1. Read the closed check-candle context from the Level 03 aggregator.
2. Rebuild the legal previous-W reference set from Level 05.
3. Read raw high/low hunt patterns for every legal reference.
4. Convert exactly-one high hunts into sell-side SMT material.
5. Convert exactly-one low hunts into buy-side SMT material.
6. Discard the entire check candle if buy-side and sell-side SMT material appear in the same check candle.
7. Select the reference that creates the largest provisional stop distance on the clean traded symbol.
8. Emit audit-only SMT candidate rows.
9. Keep all output causal: no next-candle entry price is used in this level.

## Non-scope

Level 06 does not perform:

- signal confirmation beyond the already-closed check-candle audit context,
- Entry STC ON/OFF consumption behavior,
- missed-entry handling,
- max-three-trades-per-M enforcement,
- hedging direction lock,
- paper trade simulation,
- risk volume sizing,
- broker order placement,
- partial close,
- hard close,
- chart drawing.

Those belong to later levels.

## Candidate conversion rules

### High-side SMT

A high-side SMT candidate exists when exactly one symbol touches a legal previous-W high while the other symbol does not touch its own corresponding previous-W high.

The direction is SELL.

The traded symbol is the clean symbol, meaning the one that did not hunt.

Example:

- Symbol1 touches its own W2 high.
- Symbol2 does not touch its own W2 high.
- The candidate is a SELL on Symbol2.

### Low-side SMT

A low-side SMT candidate exists when exactly one symbol touches a legal previous-W low while the other symbol does not touch its own corresponding previous-W low.

The direction is BUY.

The traded symbol is the clean symbol.

Example:

- Symbol2 touches its own W1 low.
- Symbol1 does not touch its own W1 low.
- The candidate is a BUY on Symbol1.

## Same-check ambiguity rule

If any buy-side and any sell-side SMT material exist inside the same check candle, the whole check candle is forgotten.

This means:

- no candidate is carried forward,
- no later signal is allowed from that same ambiguous check candle,
- the event is written only as an audit row with status `FORGOTTEN_SIMULTANEOUS_BUY_SELL`.

This follows the locked owner decision: if two opposing signals occur in one check candle, the strategy does not trade them and does not keep them alive for later.

## Reference selection rule

If several legal references produce SMT material for the same direction and traded symbol, Level 06 selects the reference that creates the largest provisional stop distance on the clean traded symbol.

Because Level 06 is still pre-execution and does not know the next check candle open, it uses the traded symbol's current check-candle close as the provisional entry proxy.

For sell-side candidates:

- stop reference = selected reference high of the traded symbol,
- provisional distance = reference high - traded symbol check close.

For buy-side candidates:

- stop reference = selected reference low of the traded symbol,
- provisional distance = traded symbol check close - reference low.

The selected reference is stored in the candidate audit. Later execution levels can compute actual risk from the real entry price while preserving the selected reference identity.

## Multiple same-direction candidates

If the same check candle produces only one direction, but produces candidates on both symbols, Level 06 can emit more than one audit candidate row.

Example:

- one reference creates a SELL on Symbol1,
- another reference creates a SELL on Symbol2,
- both are same direction,
- Level 06 writes both candidate rows.

The later signal/trade layer enforces max three opened trades per M and hedging rules.

## Candidate identity

Candidate IDs are deterministic and include:

- strategy ID,
- STC day ID,
- check index,
- M cycle,
- current W cycle,
- selected reference W,
- SMT side,
- direction,
- trade symbol.

The identity is not yet used for consumption in Level 06. It is prepared for Level 07 signal registry.

## Output

Level 06 writes:

`stc_level06_smt_candidates.csv`

Important columns:

- `stc_day_id`
- `check_index`
- `m_cycle`
- `current_w`
- `candidate_status`
- `candidate_id`
- `is_trade_candidate`
- `smt_side`
- `direction`
- `hunted_symbol`
- `clean_symbol`
- `trade_symbol`
- `selected_reference_w`
- `selected_reference_w_serial`
- `selected_reference_rank`
- `selected_reference_price`
- `trade_symbol_check_close`
- `provisional_stop_distance`
- `legal_reference_count`
- `high_raw_candidate_count`
- `low_raw_candidate_count`
- `same_direction_candidate_count`
- `simultaneous_buy_sell_forget`
- `status`
- `rule_note`

## Expected outputs after attach

The Common Files folder should contain:

- `stc_level06_build_sanity.csv`
- `stc_level06_runtime_events.csv`
- `stc_level06_time_audit.csv`
- `stc_level06_check_candles.csv`
- `stc_level06_w_levels.csv`
- `stc_level06_reference_hunts.csv`
- `stc_level06_smt_candidates.csv`

## Acceptance criteria

Level 06 is accepted only if:

1. It compiles.
2. It produces no trades.
3. It produces no confirmations.
4. It produces `stc_level06_smt_candidates.csv`.
5. High-side exactly-one hunts become SELL candidates on the clean symbol.
6. Low-side exactly-one hunts become BUY candidates on the clean symbol.
7. Buy and sell in the same check candle produce only a forgotten ambiguity audit row.
8. Multiple references for the same direction/trade symbol select the largest provisional stop distance.
9. W1 still produces no candidate.
10. Final check candles still produce no candidate.
