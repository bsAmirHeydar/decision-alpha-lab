# EXP0017 EN CH15 — Statistical Reporting and Metric Language

## Thesis

Reports must use measurable statistical language and include only confirmed tradeable signals in the primary sample.

## Doctrine

- Primary samples include valid confirmed tradeable signals only.
- Reports should include CG type, win rate, R:R, pip outcome, normalized pip outcome, CG overlap, and signal frequency.
- Emotional language has no place in expert reports.
- Recommended metrics may be added if they enrich statistical memory.

## Fields

- `primary_sample_flag`
- `cg_type`
- `risk_reward`
- `pip_outcome`
- `daily_range_normalized_pip`
- `signal_frequency`

## Implementation Note

- Build a report schema before AI scoring.
- Keep raw observations and primary samples separate.
