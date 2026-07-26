# Phase 02 Strategy Architect Review Checklist

Use this checklist before approving Phase 02.

- [ ] The expert compiles in MetaEditor.
- [ ] The expert sends no orders.
- [ ] Both symbols can be selected by the broker.
- [ ] M1 history is available for both symbols.
- [ ] The displayed trading day matches 18:00-17:00 New York.
- [ ] The current CG cycle is correct.
- [ ] The current cycle is not included as a reference.
- [ ] Previous same-day cycles are listed as reference candidates.
- [ ] `cg_30m` references align to 18:00, 18:30, 19:00, etc.
- [ ] Non-standard CGs still build references using M1 aggregation.
- [ ] Each reference has high and low for Symbol A and Symbol B.
- [ ] Missing data is shown as a data problem, not as market logic.
- [ ] No hunt, divergence, invalidation, entry, stop, target, risk, or ranking logic exists in this phase.
