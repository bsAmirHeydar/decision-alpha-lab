# Phase 10 — Feature Contract

## Anatomy features

- `group`
- `group_minutes`
- `current_cycle`
- `reference_cycle`
- `reference_age_cycles`
- `direction`
- `direction_code`
- `side`
- `side_code`
- `clean_symbol`
- `hunter_symbol`
- `role_key`

## Time features

- `confirmation_broker`
- `confirmation_ny`
- `hour_ny`
- `minute_of_day_ny`
- `session_ny`

## Risk geometry features

- `entry_price`
- `stop_price`
- `stop_points`
- `daily_range_points`
- `risk_to_daily_range`

## Outcome observations preserved as columns

- `cycle_end_r`
- `plus1_r`
- `plus2_r`
- `plus3_r`
- `day_end_r`
- `mfe_r`
- `mae_r`

These are historical outcome observations. Downstream modeling must prevent leakage by deciding which of these are labels and which are excluded from pre-signal features.
