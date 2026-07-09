# Phase 07 Outcome Data Contract

Each row links one confirmed signal to its forward outcomes.

## Identity fields

- `outcome_id`
- `signal_id`
- `group`
- `group_minutes`
- `current_cycle`
- `reference_cycle`
- `direction`
- `side`
- `clean_symbol`
- `hunter_symbol`
- `confirmation_broker`
- `confirmation_ny`

## Entry and risk fields

- `entry_price`
- `stop_price`
- `stop_points`

## Window fields

- cycle-end price, points, R
- +1 cycle price, points, R
- +2 cycle price, points, R
- +3 cycle price, points, R
- day-end price, points, R

## Excursion fields

- MFE price
- MFE points
- MFE R
- MAE price
- MAE points
- MAE R
- intraday stop-hit boolean
- stop-hit time

## Normalization fields

- daily range points
- day-end result divided by daily range
- MFE divided by daily range

## Availability fields

The row explicitly tells whether it is complete, pending, missing, or zero-risk.
