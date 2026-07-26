---
id: EXP0018-ADR-DY-A12
title: "EXP0018 ADR DY-A12 — Historical Line Persistence"
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
# DY-A12 — Historical Line Persistence

## سؤال

خط confirmed بعداً حذف شود؟

## وضعیت

`PROPOSED — AWAITING STRATEGY ARCHITECT APPROVAL`

## فازهای متأثر

`P08|P13`

## شواهد

Word صریحاً می‌گوید حتی اگر divergence از بین رفت خطوط نروند.

## گزینه پیشنهادی

```text
Keep confirmed line for configured lookback
```

## پیامد مهندسی

Retirement فقط future eligibility را تغییر می‌دهد.

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
