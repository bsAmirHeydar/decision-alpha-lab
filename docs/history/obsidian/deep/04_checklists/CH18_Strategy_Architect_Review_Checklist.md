# CH18 Strategy Architect Review Checklist

## Base execution law

- [ ] Entry occurs immediately after candle-close confirmation.
- [ ] No trade is taken before final confirmation.
- [ ] Divergence invalidation blocks trade permission.
- [ ] No other base restriction blocks trade permission.

## Position limits

- [ ] There is no base total-position limit.
- [ ] There is no base same-CG position limit.
- [ ] There is no base same-symbol position limit.
- [ ] There is no base same-direction position limit.
- [ ] There is no base opposite-direction or hedge ban.

## Repeated signals

- [ ] A losing cycle does not block the next cycle.
- [ ] A prior stop-out does not create a cooldown rule.
- [ ] Multiple positions from one CG are allowed.
- [ ] Same-CG repetition is measured, not manually rejected.

## Research requirements

- [ ] Position clusters are tracked.
- [ ] Hedge cases are tracked.
- [ ] Same-CG repetition is tracked.
- [ ] Signal sequence number is tracked.
- [ ] Prior outcome context is tracked.
- [ ] Future constraints are treated as hypotheses only.

## AI/model boundary

- [ ] Model may rank no-limit execution families.
- [ ] Model may suggest constraints after analysis.
- [ ] Model cannot impose constraints automatically.
- [ ] Strategy architect remains final authority.
