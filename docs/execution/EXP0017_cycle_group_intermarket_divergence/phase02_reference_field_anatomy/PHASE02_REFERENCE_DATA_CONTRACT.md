# Phase 02 Reference Data Contract

## Reference pair

Each reference pair represents the same CG cycle for both symbols.

Required fields:

```text
group_name
group_minutes
reference_cycle_index
reference_cycle_number
start_minute
end_minute_exclusive
cycle_start_ny
cycle_end_ny
cycle_start_broker
cycle_end_broker
complete_cycle
ready
symbol_a_reference
symbol_b_reference
```

## Symbol reference

Each symbol reference must preserve:

```text
symbol
selected
data_ok
copied_bars
high
low
first_bar_broker
last_bar_broker
error_text
```

## Ready condition

A reference pair is ready only if both symbols have usable M1 bars for the same cycle window:

```text
symbol_a.data_ok == true
symbol_b.data_ok == true
```

If one side is missing, the pair is not ready for future hunt comparison.

## Missing data is not a market signal

Missing M1 data must never be interpreted as:

- no hunt
- clean symbol
- divergence
- invalidation
- weakness
- strength

It is only a data-readiness problem.

## Field preservation

Future phases should preserve these references rather than recomputing time boundaries independently.

Phase 03 Hunt Anatomy should consume this field as its input.
