# Phase 03 Strategy Architect Review Checklist

Use this checklist before approving Phase 03 and moving to Phase 04.

## Hunt definition

- [ ] High hunt uses `current_high >= reference_high`.
- [ ] Low hunt uses `current_low <= reference_low`.
- [ ] Equality counts as hunt.
- [ ] Close beyond the reference is not required.
- [ ] Wick/touch behavior is sufficient.

## Reference integrity

- [ ] References come from Phase 02.
- [ ] References are same-day only.
- [ ] References are completed previous CG cycles only.
- [ ] Current cycle is not a reference.
- [ ] Symbol A is compared only to Symbol A references.
- [ ] Symbol B is compared only to Symbol B references.

## Boundary integrity

- [ ] No divergence labels exist.
- [ ] No buy/sell signals exist.
- [ ] No candle-close confirmation exists.
- [ ] No invalidation logic is applied.
- [ ] No trade orders exist.
- [ ] No ranking or filtering exists.

## Display integrity

- [ ] H means high hunted.
- [ ] L means low hunted.
- [ ] H+L means both high and low hunted by that symbol against that reference.
- [ ] One-symbol and both-symbol hunt states are visible.
- [ ] Missing data is shown as missing, not as clean behavior.
