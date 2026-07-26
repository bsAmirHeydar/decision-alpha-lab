# EXP0017 — Implementation Sequence Checklist

## Before Code

- Master doctrine exists.
- Forbidden assumptions are explicit.
- Statistical-only boundary is explicit.
- AI non-mutation boundary is explicit.
- Field catalog is available.

## Anatomy Phase Gates

- Time anatomy validates New York 18:00-to-17:00 days.
- Reference anatomy validates all previous same-day cycles.
- Hunt anatomy validates equality, touch, and break logic.
- Divergence anatomy validates hunter/clean asymmetry.
- Confirmation validates candle-close timing.
- Invalidation validates double-hunt cases.

## Statistical Phase Gates

- Ledger stores only confirmed tradeable signals in the primary sample.
- Outcome engine calculates multiple windows, not only cycle-end close.
- Reports separate CG, direction, symbol role, session, overlap, and density families.
- Model dataset preserves raw fields and future features.

## Execution Gates

- Raw execution can be built only after anatomy and ledger are stable.
- Filtered execution can be built only after statistical promotion.
- AI can rank and compare but cannot directly execute or mutate strategy.
