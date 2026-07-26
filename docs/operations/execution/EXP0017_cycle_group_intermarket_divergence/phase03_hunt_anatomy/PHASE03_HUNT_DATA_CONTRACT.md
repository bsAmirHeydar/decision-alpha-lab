# Phase 03 Hunt Data Contract

## Group-level fields

Each enabled CG produces a group state:

```text
group_name
group_minutes
current_cycle_number
previous_cycle_count
ready_reference_count
missing_reference_count
ready_current_range_count
any_hunt_count
high_hunt_count
low_hunt_count
symbol_a_hunt_count
symbol_b_hunt_count
one_symbol_high_hunt_count
one_symbol_low_hunt_count
both_symbol_high_hunt_count
both_symbol_low_hunt_count
```

These fields are descriptive only.

## Reference-level fields

For every previous same-day reference cycle:

```text
reference_cycle_number
reference_cycle_start_ny
reference_cycle_end_ny
reference_ready
current_range_ready
symbol_a.high_hunted
symbol_a.low_hunted
symbol_b.high_hunted
symbol_b.low_hunted
high_hunted_by_one_symbol_only
low_hunted_by_one_symbol_only
high_hunted_by_both_symbols
low_hunted_by_both_symbols
```

## Symbol-level fields

For each symbol:

```text
reference_high
reference_low
current_high
current_low
high_hunted
low_hunted
any_hunt
status_text
```

## Important interpretation boundary

A one-symbol high hunt can later become sell-divergence input. A one-symbol low hunt can later become buy-divergence input.

But Phase 03 does not create divergence labels.

It stores the raw condition only.

## Missing data rule

If M1 data is missing, the system must record missing data.

It must not convert missing data into:

```text
not hunted
clean symbol
valid asymmetry
divergence
weakness
strength
```
