---
id: EXP0018-ADR-DY-A03
title: "EXP0018 ADR DY-A03 — Weekly Boundary"
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
# DY-A03 — Weekly Boundary

## سؤال

مرز W چیست؟

## وضعیت

`PROPOSED — AWAITING STRATEGY ARCHITECT APPROVAL`

## فازهای متأثر

`P03|P04|P13`

## شواهد

Word مرز دقیق نمی‌دهد؛ قرارداد futures نیازمند boundary صریح است.

## گزینه پیشنهادی

```text
Sunday 18:00 NY to Friday 16:59:59 NY
```

## پیامد مهندسی

تا تصویب WW disabled می‌ماند.

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
