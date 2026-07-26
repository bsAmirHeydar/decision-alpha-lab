---
id: EXP0018-ADR-DY-A10
title: "EXP0018 ADR DY-A10 — Triad Authority"
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
# DY-A10 — Triad Authority

## سؤال

Triad در v1 چه اختیاری دارد؟

## وضعیت

`PROPOSED — AWAITING STRATEGY ARCHITECT APPROVAL`

## فازهای متأثر

`P19`

## شواهد

Word ورودی دو نماد دارد؛ QT triad را context می‌دهد.

## گزینه پیشنهادی

```text
Observer only
```

## پیامد مهندسی

Triad حق invalidate کردن pair signal ندارد.

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
