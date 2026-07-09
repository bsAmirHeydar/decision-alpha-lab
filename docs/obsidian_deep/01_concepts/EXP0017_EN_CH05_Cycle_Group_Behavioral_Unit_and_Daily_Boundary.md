# EXP0017 EN CH05 — Cycle Group Behavioral Unit and Daily Boundary

## Thesis

Each cycle group is an independent behavioral unit anchored to the 18:00 New York trading-day boundary.

## Doctrine

- The trading day begins at 18:00 New York and ends at 17:00 New York.
- Each CG is a family of potential divergence behavior.
- All CGs are allowed in the base version.
- No CG is stronger or weaker before statistics.

## Fields

- `cg_name`
- `cg_minutes`
- `trading_day_start_ny`
- `cycle_index`
- `cycle_boundary`

## Implementation Note

- Build the CG calendar before reference and hunt logic.
- Avoid CG ranking in the base implementation.
