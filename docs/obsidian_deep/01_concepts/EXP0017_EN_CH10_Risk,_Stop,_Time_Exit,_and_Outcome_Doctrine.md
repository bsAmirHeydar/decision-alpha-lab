# EXP0017 EN CH10 — Risk, Stop, Time Exit, and Outcome Doctrine

## Thesis

Risk is fixed in the base version, stop is absolute at the clean reference, and the initial target concept is time-based.

## Doctrine

- Base risk is fixed at 1% equity.
- Stop price is the clean symbol reference level.
- No quality-based risk adjustment exists before statistics.
- Cycle-end exit is the base time target, but later studies may add alternative targets.
- Dollar result is an important statistical outcome.

## Fields

- `risk_percent`
- `stop_price`
- `stop_distance`
- `cycle_end_time`
- `dollar_outcome`
- `r_outcome`

## Implementation Note

- Separate stop logic from model scoring.
- Record multiple outcome windows even if base exit remains cycle-end.
