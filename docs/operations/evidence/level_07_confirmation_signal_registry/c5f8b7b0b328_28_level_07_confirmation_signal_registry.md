# Level 07 — Confirmation and Signal Registry

## Purpose

Level 07 converts the audit-only SMT candidates from Level 06 into an audit-only signal registry. It still does not place paper trades and it still does not send real orders.

This level is the first layer where the strategy speaks in terms of a confirmed STC signal rather than a raw hunt or a raw SMT candidate.

The locked owner rule is that the signal only exists at the close of a valid check candle. If the expert was offline at that exact entry moment, the system must never enter later because the stop quality is no longer the same. Level 07 records such situations as audit-only consumed rows.

## Inputs Added

- `InpWriteSignalRegistryAudit`
- `InpMaxSignalBackfillOnInit`
- `InpMaxSignalCatchupPerPulse`

These inputs control the signal registry audit output. They do not enable trading.

## New MQL5 Module

- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Signals.mqh`

The module depends on the Level 06 candidate engine and registers closed-check signal rows.

## New Output File

Common Files path:

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level07_signal_registry.csv`

This file is the main output of Level 07.

## Signal Registry Rules

A signal row is created only from a closed check candle.

A valid signal must have:

1. A valid STC trading day.
2. A check candle whose start is inside an active M cycle.
3. A check candle that is not the final check candle of its M.
4. Complete data for both symbols.
5. A legal previous-W reference set.
6. An SMT candidate from exactly-one-symbol high or low hunt.
7. A positive provisional stop distance on the clean traded symbol.
8. No simultaneous buy-side and sell-side SMT in the same check candle.

## Confirmation Meaning

Level 07 treats the closed check candle itself as the confirmation moment.

There is no extra delayed confirmation candle. The strategy already waited until the check candle close before allowing a candidate to become a signal.

## Entry OFF Rule

If `Entry STC` is OFF at the confirmation moment:

- The signal is written to audit.
- No trade is placed.
- The signal is consumed.
- The signal is not allowed to enter later if `Entry STC` is turned back ON.

The output status is:

`CONFIRMED_ENTRY_OFF_CONSUMED`

## Offline / Late Entry Rule

If the expert was offline at the exact check-close entry moment, Level 07 still reconstructs the signal for audit if the candle data exists, but it marks it as late/missed.

The signal remains audit-only and cannot be entered later.

This preserves the locked rule that no delayed entry is allowed.

## Simultaneous Buy and Sell Rule

If a buy-side SMT and sell-side SMT are both present in the same check candle, the whole check candle is forgotten.

No signal is carried forward.

The output status is:

`FORGOTTEN_SIMULTANEOUS_BUY_SELL`

## Final Check Candle Rule

If the check candle closes at the end of an M cycle, it is not eligible for entry.

It can be audited, but it cannot become an executable signal.

The output status is:

`REJECTED_FINAL_CHECK_NO_ENTRY`

## Signal Consumption

Every signal registry row is treated as consumed. This is intentional.

The strategy must never enter on a later check candle just because the same divergence still exists. A signal belongs to the exact check-close moment only.

## No Trading in Level 07

Level 07 never increments a trade counter and never attempts an order.

These fields are always false in this level:

- `order_attempted`
- `trade_counter_incremented`

Paper execution begins in a later level.

## Important Columns

`signal_status` describes the final registry status.

`signal_id` is the deterministic signal identity.

`source_candidate_id` points back to the Level 06 SMT candidate.

`is_confirmed_signal` tells whether a real confirmed signal existed.

`signal_consumed` is true for all registry outcomes to prevent delayed entries.

`entry_stc_enabled_at_confirmation` records the STC Entry switch at the confirmation moment.

`entry_missed_or_late` marks signals that were reconstructed after the EA had already missed their entry moment.

`selected_reference_w` is the selected previous W reference.

`provisional_stop_distance` is still provisional; exact paper/live risk is deferred to later levels.

## Acceptance Criteria

Level 07 is accepted when:

- The EA compiles.
- `stc_level07_signal_registry.csv` is created.
- Valid Level 06 candidates appear as Level 07 signal rows.
- Entry OFF creates audit-only consumed rows.
- Final check candles do not become executable signals.
- Same-check buy and sell are forgotten.
- No orders are placed.
- No paper trades are created.
- No trade counter is incremented.
