---
id: EXP0018-ADR-DY-A05
title: "EXP0018 ADR DY-A05 — NP Relationship"
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
# DY-A05 — NP Relationship

## سؤال

NP کدام Periodها را مقایسه می‌کند؟

## وضعیت

`PROPOSED — AWAITING STRATEGY ARCHITECT APPROVAL`

## فازهای متأثر

`P04|P13`

## شواهد

زنجیره PA/AL/LN/NP این تفسیر را تقویت می‌کند.

## گزینه پیشنهادی

```text
Current P vs immediately preceding N in same trading day
```

## پیامد مهندسی

در صورت عدم تصویب NP disabled.

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
