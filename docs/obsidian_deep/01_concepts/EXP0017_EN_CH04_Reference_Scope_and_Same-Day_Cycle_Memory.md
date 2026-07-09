# EXP0017 EN CH04 — Reference Scope and Same-Day Cycle Memory

## Thesis

All previous cycles from the same New York trading day are valid reference candidates until invalidated or day-expired.

## Doctrine

- Reference candidates are the high and low of previous cycles in the same CG and same trading day.
- No previous-day reference is used for live decision.
- No reference hierarchy is assumed before statistics.
- A reference becomes invalid for divergence only when the asymmetry is removed by double hunt.

## Fields

- `reference_cycle_start`
- `reference_cycle_end`
- `reference_age_cycles`
- `same_day_reference_index`
- `reference_status`

## Implementation Note

- The reference field must store all previous same-day cycle highs/lows.
- The engine must not use yesterday’s references for live signals.
