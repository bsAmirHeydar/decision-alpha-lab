---
id: EXP0018-ADR-DY-A04
title: "EXP0018 ADR DY-A04 — First Sweep Scope"
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
# DY-A04 — First Sweep Scope

## سؤال

مصرف نخستین sweep با چه کلیدی اعمال شود؟

## وضعیت

`PROPOSED — AWAITING STRATEGY ARCHITECT APPROVAL`

## فازهای متأثر

`P07|P13`

## شواهد

Word first sweep را canonical می‌داند؛ PDFها repeated contexts دارند.

## گزینه پیشنهادی

```text
relationship+reference period+side+hunter/protected
```

## پیامد مهندسی

Reference-side و opportunity identity جدا نگه داشته شوند.

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
