# EXP0017 EN CH07 — Time Validity, Cash Session, and Stop Pressure

## Thesis

All times are valid before statistics; the 09:30–16:00 New York cash session is a hypothesis, not a hard rule.

## Doctrine

- Cash session may produce stronger statistics but is not a pre-test filter.
- No sub-session split is mandatory in the base version.
- News is not a base filter.
- Stop-size pressure across CGs is a market condition worth recording.

## Fields

- `cash_session_flag`
- `time_from_cash_open`
- `time_to_cash_close`
- `stop_distance`
- `cg_stop_pressure_rank`

## Implementation Note

- Record session state from day one.
- Do not block non-cash-session signals.
