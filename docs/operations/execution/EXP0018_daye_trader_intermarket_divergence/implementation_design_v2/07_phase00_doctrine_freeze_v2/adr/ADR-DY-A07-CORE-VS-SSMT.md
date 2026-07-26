---
id: EXP0018-ADR-DY-A07
title: "EXP0018 ADR DY-A07 — Core 22 vs SSMT"
type: ADR
status: proposed
project: EXP0018
version: 2.1.0
created: 2026-07-10
updated: 2026-07-10
owner: Strategy Architect
tags:
  - exp0018
  - daye-trader
  - phase00
  - doctrine-freeze
---
# DY-A07 — Core 22 vs SSMT

## سؤال

۲۲ رابطه با SSMT taxonomy ادغام شوند؟

## وضعیت

`PROPOSED — AWAITING STRATEGY ARCHITECT APPROVAL`

## فازهای متأثر

`P04|P16`

## شواهد

۲۲ رابطه محصولی canonical است؛ SSMT corpus گسترده‌تر و research است.

## گزینه پیشنهادی

```text
Keep 22 Core relationships independent
```

## پیامد مهندسی

Optional engine consumer Core events است، نه owner آنها.

## گزینه‌های ردشده یا جایگزین

- Alternative A: باید تعریف و مثال مثبت/منفی داشته باشد.
- Alternative B: باید اثر schema، replay و migration آن نوشته شود.
- Defer: feature وابسته disabled می‌ماند.

## Fixtureهای لازم

- positive case
- exact-boundary/equality case
- counterexample
- partial-data case where applicable
- restart/replay idempotency case

## تصمیم نهایی

```text
Decision: PENDING
Approved by:
Approved at:
Doctrine version:
Rationale:
```
