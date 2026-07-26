# EXP0017 EN CH11 — Cycle Group Independence and Daily Reset

## Thesis

CGs, directions, and daily fields are independent in the base layer; previous days do not carry decision authority.

## Doctrine

- Buy and sell are both valid research families.
- CGs do not validate or cancel each other before statistics.
- No confluence assumption exists before testing.
- Every day is independent from previous days for live decision.

## Fields

- `trading_day`
- `cg_name`
- `direction`
- `same_day_signal_count`
- `previous_day_carryover_flag`

## Implementation Note

- Implement same-day decision memory and research memory separately.
- Do not carry references from prior days into live signal construction.
