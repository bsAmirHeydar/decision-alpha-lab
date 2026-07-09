# EXP0017 EN CH18 — Execution Freedom and Position Multiplicity

## Thesis

The base execution field has no position-count limit, allows repeated CG opportunities, and permits hedging unless statistics later justify constraints.

## Doctrine

- Multiple positions from one CG are allowed.
- Loss in one cycle does not block the next cycle.
- Hedging is allowed in the base layer.
- Immediate entry after final confirmation is the base timing.
- Only invalidation at confirmation blocks trade permission.

## Fields

- `open_position_count`
- `same_cg_position_count`
- `hedge_state`
- `post_loss_signal_flag`
- `entry_after_confirmation`

## Implementation Note

- Raw execution must preserve signal freedom.
- Future exposure constraints are statistical hypotheses, not base filters.
