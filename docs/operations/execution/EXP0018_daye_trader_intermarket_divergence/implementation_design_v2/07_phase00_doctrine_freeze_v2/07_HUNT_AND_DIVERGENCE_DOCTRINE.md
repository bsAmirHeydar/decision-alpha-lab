---
id: EXP0018-P00-HUNT
title: "EXP0018 Phase 00 — Hunt and Divergence Doctrine"
type: specification
status: draft
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

# دکترین Hunt و Divergence

## Hunt سمت High

برای هر نماد جداگانه:

```text
current_high >= reference_high
```

Equality یک Hunt معتبر است.

## Hunt سمت Low

```text
current_low <= reference_low
```

Equality یک Hunt معتبر است.

## One-sided divergence

برای یک Relationship و یک side:

```text
symbol_a_hunted XOR symbol_b_hunted
```

- نماد با `true` = Hunter
- نماد با `false` = Protected

اگر هر دو false باشند، divergence وجود ندارد. اگر هر دو true باشند، Double Hunt است.

## Direction label

Mapping High/Low به BUY/SELL در source تعارض دارد و تا ADR-DY-A01 نهایی نشود، detector باید `SIDE_HIGH` و `SIDE_LOW` تولید کند؛ label جهت می‌تواند disabled بماند.

## ممنوعیت‌ها

- close پشت سطح برای Hunt لازم نیست.
- مقایسه قیمت خام دو نماد ممنوع است.
- wick-touch با body/close divergence یکی نیست.
- Hunt observation اجازه رسم مستقیم ندارد.
- missing data نباید false شود.
