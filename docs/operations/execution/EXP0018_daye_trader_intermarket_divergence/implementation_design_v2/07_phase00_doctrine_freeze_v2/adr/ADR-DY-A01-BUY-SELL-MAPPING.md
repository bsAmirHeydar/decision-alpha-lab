---
id: EXP0018-ADR-DY-A01
title: "EXP0018 ADR DY-A01 — BUY/SELL Mapping"
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
# DY-A01 — BUY/SELL Mapping

## سؤال

آیا High-side به SELL و Low-side به BUY نگاشت شود؟

## وضعیت

`PROPOSED — AWAITING STRATEGY ARCHITECT APPROVAL`

## فازهای متأثر

`P04|P05|P13`

## شواهد

Word متن و مثال متعارض دارد؛ مثال LN high برای sell را نشان می‌دهد.

## گزینه پیشنهادی

```text
High-side=SELL; Low-side=BUY
```

## پیامد مهندسی

Core می‌تواند تا تصویب فقط SIDE_HIGH/SIDE_LOW تولید کند.

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
