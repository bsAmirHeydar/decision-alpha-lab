---
id: EXP0018-P00-RELATIONSHIPS
title: "EXP0018 Phase 00 — Relationship Doctrine"
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

# دکترین ۲۲ رابطه

## قرارداد کلی

هر Relationship یک رکورد declarative با این فیلدهاست:

```text
relationship_id
source_alias
family
current_period_type
reference_period_type
reference_selector
major
chart_label
enabled
source_authority
schema_version
```

## شش رابطه بزرگ

| Alias | Current | Reference | وضعیت |
|---|---|---|---|
| WW | W فعلی | W قبلی | boundary هفتگی blocker |
| DD | D فعلی | D قبلی | قابل تثبیت |
| PA | A فعلی | P قبلی | قابل تثبیت |
| AL | L فعلی | A قبلی | قابل تثبیت |
| LN | N فعلی | L قبلی | قابل تثبیت |
| NP | P فعلی | N بلافاصله قبل | پیشنهادی؛ ADR-DY-A05 |

## شانزده رابطه 90m

```text
A1←P4, A2←A1, A3←A2, A4←A3
L1←A4, L2←L1, L3←L2, L4←L3
N1←L4, N2←N1, N3←N2, N4←N3
P1←N4, P2←P1, P3←P2, P4←P3
```

## قواعد

- Current و Reference با ID period instance resolve می‌شوند، نه با «کندل قبلی» مبهم.
- هر Relationship مستقل ارزیابی می‌شود.
- وجود چند Relationship در یک Close مجاز است.
- BUY و SELL هم‌زمان در Relationshipهای متفاوت می‌تواند وجود داشته باشد.
- ۲۲ رابطه Core از taxonomy گسترده SSMT جدا می‌ماند تا ADR-DY-A07 تصویب شود.
- Majorها label دارند؛ Minorها فقط line.
