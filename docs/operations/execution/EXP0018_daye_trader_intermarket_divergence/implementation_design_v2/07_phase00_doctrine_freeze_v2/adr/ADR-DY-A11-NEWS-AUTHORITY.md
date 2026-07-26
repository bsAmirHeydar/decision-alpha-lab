---
id: EXP0018-ADR-DY-A11
title: "EXP0018 ADR DY-A11 — News Authority"
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
# DY-A11 — News Authority

## سؤال

خبر context است یا filter؟

## وضعیت

`PROPOSED — AWAITING STRATEGY ARCHITECT APPROVAL`

## فازهای متأثر

`P18|P20`

## شواهد

PDFها خبر را مهم می‌دانند اما Core نباید به اینترنت وابسته باشد.

## گزینه پیشنهادی

```text
Ledger-only context in v1
```

## پیامد مهندسی

فیلتر فقط پس از outcome study و promotion.

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
