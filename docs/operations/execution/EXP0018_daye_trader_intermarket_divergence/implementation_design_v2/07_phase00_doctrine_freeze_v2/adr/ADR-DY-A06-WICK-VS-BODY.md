---
id: EXP0018-ADR-DY-A06
title: "EXP0018 ADR DY-A06 — Wick vs Body Scope"
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
# DY-A06 — Wick vs Body Scope

## سؤال

Core فقط wick-touch باشد؟

## وضعیت

`PROPOSED — AWAITING STRATEGY ARCHITECT APPROVAL`

## فازهای متأثر

`P00|P16`

## شواهد

Word touch-only canonical؛ Trader Daye body/close را variant جدا مطرح می‌کند.

## گزینه پیشنهادی

```text
Core=wick touch only; body/close=P16 typed event
```

## پیامد مهندسی

از boolean مبهم SMT جلوگیری می‌شود.

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
