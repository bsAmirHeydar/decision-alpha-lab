---
id: EXP0018-P00-LIFECYCLE
title: "EXP0018 Phase 00 — Reference Lifecycle Doctrine"
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

# دکترین چرخه عمر Reference

## Stateهای پیشنهادی

```text
DISCOVERED
ACTIVE
ONE_SIDED_HUNTED
CONFIRMED_USED
PROTECTED_SURVIVES
PROTECTED_BREACHED
CONSUMED
RETIRED
UNAVAILABLE
```

## دو هویت متفاوت

### Reference Side Identity

```text
symbol + reference_period_instance_id + side
```

این هویت می‌گوید یک high/low مشخص در یک نماد چیست.

### Divergence Opportunity Identity

```text
relationship_id
+ current_period_instance_id
+ reference_period_instance_id
+ side
+ hunter_symbol
+ protected_symbol
```

این هویت می‌گوید یک فرصت خاص کدام است.

## First Sweep

منبع اصلی می‌گوید اگر یک سطح چند بار sweep شد، فقط دفعه اول مهم است. دامنه دقیق مصرف هنوز نیازمند ADR-DY-A04 است.

پیشنهاد پایه:

1. اولین confirmation معتبر برای یک Opportunity Key ثبت شود.
2. همان Opportunity Key دوباره تأیید نشود.
3. تا وقتی Protected سطح خودش را نزده، reference-side از نظر pair زنده است؛ اما duplicate همان opportunity مجاز نیست.
4. وقتی Protected سطح خودش را بزند، pair-side برای آن relationship/reference retire شود.
5. role-switch روی همان pair-side سیگنال تازه محسوب نشود مگر ADR خلاف آن را تصویب کند.

## اصل بازگشت‌ناپذیری

```text
RETIRED → ACTIVE ممنوع
CONSUMED → ACTIVE ممنوع
```

بازسازی state پس از restart باید از ledger یا replay deterministic همان نتیجه را تولید کند.
