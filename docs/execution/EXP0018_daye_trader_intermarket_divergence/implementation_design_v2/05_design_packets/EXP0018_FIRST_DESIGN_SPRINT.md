  ---
  id: EXP0018-FIRST-DESIGN-SPRINT
  title: "EXP0018 First Design Sprint"
  type: plan
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---

# اولین Sprint طراحی

هدف Sprint اول: **P00 را ببندیم و P01/P02 را Code-Ready کنیم؛ نه اینکه هنوز detector بنویسیم.**

## جلسه 1 — Doctrine blockers

خروجی: پاسخ قطعی DY-A01، DY-A02، DY-A03، DY-A04، DY-A05، DY-A12.

## جلسه 2 — Time contract review

- تطبیق P01 موجود با ساعت‌های canonical
- fixtureهای DST و boundary
- تصمیم Weekly period

## جلسه 3 — Data synchronization design

- نمادهای ورودی و suffix
- base timeframe
- missing bar policy
- canonical timestamp alignment

## جلسه 4 — Period schema

- period IDs
- completeness
- previous/current links
- O/H/L/C aggregation

## جلسه 5 — 22 registry table

- canonical IDs
- current/reference pairs
- major/minor label
- enable flags
- source traceability

## Exit criteria

P00 = CLOSED، P01 = VERIFIED DESIGN، P02/P03/P04 = CODE-READY DESIGN.
