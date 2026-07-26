---
id: EXP0018-ADR-DY-A08
title: "EXP0018 ADR DY-A08 — Extended True Opens Placement"
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
# DY-A08 — Extended True Opens Placement

## سؤال

True Openهای گسترش‌یافته کجا باشند؟

## وضعیت

`PROPOSED — AWAITING STRATEGY ARCHITECT APPROVAL`

## فازهای متأثر

`P14`

## شواهد

Core Word فقط TWO/TDO محصولی را می‌خواهد.

## گزینه پیشنهادی

```text
Separate optional module/expert
```

## پیامد مهندسی

Dependency از Optional به Core ممنوع.

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
