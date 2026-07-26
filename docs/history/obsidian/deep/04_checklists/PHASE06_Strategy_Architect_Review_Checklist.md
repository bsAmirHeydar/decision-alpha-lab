# Phase 06 Strategy Architect Review Checklist

## Visual audit

- [ ] Objects use the `EXP0017_P06_` prefix.
- [ ] Confirmed states are drawn only when configured.
- [ ] Invalidated double-hunt states are drawn only when configured.
- [ ] Labels show CG, direction, hunter, clean symbol, and reference cycle.
- [ ] Chart-symbol scale caveat is understood.
- [ ] Hunter-chart-only mode behaves correctly.

## Ledger audit

- [ ] CSV ledger is created when enabled.
- [ ] Header is written once.
- [ ] Confirmed states are written when configured.
- [ ] Invalidated states are written when configured.
- [ ] Duplicate rows are blocked on repeated timer/tick pulses.
- [ ] Ledger rows are not treated as performance results.

## Phase boundary

- [ ] No order execution exists.
- [ ] No risk calculation exists.
- [ ] No target logic exists.
- [ ] No outcome statistics exist.
- [ ] No model scoring exists.
