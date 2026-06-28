# Level 05 — Reference Matrix and Raw Hunt Detector

## Purpose

Level 05 adds the first market-condition detector for `EXEC001_STC_SMT_Cycles`.

It does **not** create SMT candidates yet. It does **not** confirm signals. It does **not** simulate trades. It does **not** place orders.

This level only answers one question for every closed check candle:

> Against each legal previous-W reference inside the same M, did Symbol1 and/or Symbol2 touch the reference high or low?

The output is a raw reference-hunt audit stream. Later levels will convert these raw hunts into SMT divergence candidates, then confirmation events, then paper trades, then optional live orders.

## Locked owner rules implemented in this level

Level 05 implements these locked rules:

- W1 never produces a signal.
- W2 may compare only with W1.
- W3 may compare only with W2 and W1.
- W4 may compare only with W3, W2, and W1.
- No W may compare with itself.
- References are always from the same M.
- Symbol1 and Symbol2 each use their own W levels.
- The comparison is structural, not price-shared.
- Touch equality is valid.
- High hunt means `check_high >= reference_high`.
- Low hunt means `check_low <= reference_low`.
- There is no tolerance.
- Both symbols must have complete check-candle data.
- Both symbols must have complete reference-W data.
- Gap checks do not extract signal data.
- Final check candle of each M is audited but cannot become an entry source.
- Level 05 remains raw audit only.

## Reference matrix

The legal matrix is:

| Current W | Legal previous-W references | Audit order |
|---|---:|---|
| W1 | none | W1 has no signal |
| W2 | W1 | W1 |
| W3 | W2, W1 | nearest first |
| W4 | W3, W2, W1 | nearest first |

The audit order is nearest previous W first, but Level 05 does not select the final strategy reference. The locked strategy reference selection rule says later levels must choose the reference that creates the **largest stop distance on the clean/traded symbol**. Level 05 therefore records every legal reference so that the later selector can choose correctly.

## Raw hunt definitions

For every legal reference W:

### Symbol1 high hunt

Symbol1 high hunt is true when:

`symbol1_check_high >= symbol1_reference_W_high`

### Symbol1 low hunt

Symbol1 low hunt is true when:

`symbol1_check_low <= symbol1_reference_W_low`

### Symbol2 high hunt

Symbol2 high hunt is true when:

`symbol2_check_high >= symbol2_reference_W_high`

### Symbol2 low hunt

Symbol2 low hunt is true when:

`symbol2_check_low <= symbol2_reference_W_low`

No close condition is used. No buffer is used. No tolerance is used.

## Hunt patterns

For the high side and the low side, Level 05 derives a pattern:

- `NONE`: neither symbol touched the reference level.
- `SYMBOL1_ONLY`: only Symbol1 touched.
- `SYMBOL2_ONLY`: only Symbol2 touched.
- `BOTH`: both symbols touched.

`SYMBOL1_ONLY` and `SYMBOL2_ONLY` are raw exactly-one-symbol conditions. They are necessary for SMT, but they are not yet confirmed SMT signals in Level 05.

## Why Level 05 does not create SMT signals yet

A raw exactly-one-symbol hunt is not enough to execute the strategy.

Later levels still need to apply:

- SMT candidate identity rules.
- simultaneous buy/sell ambiguity rules.
- confirmation at check-candle close.
- one-trade-per-divergence registry.
- Entry STC ON/OFF rules.
- hedging and per-M direction lock.
- max-three-trades-per-M constraints.
- largest-stop reference selection for final risk placement.

Keeping Level 05 raw prevents accidental signal generation before the audit layer is verified.

## Output file

Level 05 writes:

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level05_reference_hunts.csv`

Each row is one check-candle/reference-W audit row.

Important columns:

- `stc_day_id`
- `check_index`
- `check_start_ny`
- `check_end_ny`
- `m_cycle`
- `current_w`
- `reference_w`
- `reference_rank`
- `detection_allowed_for_signal`
- `entry_allowed_at_close`
- `final_check_of_m`
- `check_pair_data_complete`
- `reference_pair_data_complete`
- `pair_data_complete`
- Symbol1 reference high/low
- Symbol1 check high/low
- Symbol1 high/low hunt flags
- Symbol2 reference high/low
- Symbol2 check high/low
- Symbol2 high/low hunt flags
- high hunt pattern
- low hunt pattern
- exactly-one high/low flags
- high hunted/clean symbol
- low hunted/clean symbol
- status
- rule note

## Status values

Expected status values include:

- `check_start_in_gap_no_detection_no_data_extraction`
- `check_not_detection_eligible_final_or_invalid`
- `check_pair_data_incomplete_no_hunt_detection`
- `no_legal_previous_W_reference_W1_has_no_signal`
- `reference_pair_data_incomplete_no_hunt_detection`
- `raw_hunt_audited_no_signal_generated`

## Acceptance criteria

Level 05 is accepted when:

1. The EA compiles.
2. Level 01 to Level 04 outputs still write normally.
3. `stc_level05_reference_hunts.csv` is created when hunt audit is enabled.
4. W1 check candles produce no-reference rows.
5. W2 check candles compare only with W1.
6. W3 check candles compare only with W2 and W1.
7. W4 check candles compare only with W3, W2, and W1.
8. Gap checks do not extract signal data.
9. Final check candle rows cannot become entry-eligible.
10. Equality touch is treated as a hunt.
11. No SMT candidate, confirmation, signal, paper trade, or order is created.

## Next level

Level 06 should convert raw hunts into SMT candidate objects.

That level should use the Level 05 audit rows conceptually, but in code it should use the same underlying structures directly. Level 06 will decide:

- high-side exactly-one hunt becomes a raw sell-side SMT candidate;
- low-side exactly-one hunt becomes a raw buy-side SMT candidate;
- trade symbol is the clean non-hunted symbol;
- simultaneous buy/sell in one check candle is forgotten and not traded;
- candidate identity prevents duplicate entries in later confirmation levels.
