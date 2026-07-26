# Phase 04 Divergence Data Contract

Each divergence candidate must preserve enough information for future confirmation, invalidation, drawing, signal ledger, and statistical reporting.

## Required candidate fields

```text
divergence_id
group_name
group_minutes
current_cycle_index
current_cycle_number
reference_cycle_index
reference_cycle_number
trading_day_start_ny
trading_day_end_ny
current_cycle_start_ny
current_cycle_end_ny
reference_cycle_start_ny
reference_cycle_end_ny
direction
side
status
hunter_symbol
clean_symbol
symbol_a_is_hunter
symbol_b_is_hunter
one_sided_hunt
both_symbols_hunted_same_side
data_ready
hunter_reference_price
clean_reference_price
hunter_current_extreme
clean_current_extreme
clean_stop_reference_price
note
```

## Status values

```text
CANDIDATE
SYMMETRIC_HUNT_NO_DIVERGENCE
MISSING_DATA
NONE
```

## Why candidate is not signal

A Phase 04 candidate is not yet a tradeable signal because final confirmation requires the active chart timeframe candle close.

The next phase must decide whether a candidate survives until confirmation.
