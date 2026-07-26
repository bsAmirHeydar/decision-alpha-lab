---
id: EXP0018-ADR-DY-A02
title: "EXP0018 ADR DY-A02 — TWO Anchor"
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
# DY-A02 — TWO Anchor

## سؤال

TWO دقیقاً از کدام زمان شروع می‌شود؟

## وضعیت

`PROPOSED — AWAITING STRATEGY ARCHITECT APPROVAL`

## فازهای متأثر

`P10|P13`

## شواهد

QT Education p9 این تعریف را صریح دارد؛ Word wording مبهم است.

## گزینه پیشنهادی

```text
Tuesday trading-day open = Monday 18:00 NY
```

## پیامد مهندسی

Anchor باید time-based باشد و به broker label وابسته نباشد.

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
