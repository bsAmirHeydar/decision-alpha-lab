---
title: "23 — Signal Identity، Dedup و Ledger"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 23 — Signal Identity، Dedup و Ledger

## event identity material

```text
context_id/version
pair_id and exact symbols/contracts
relation_code
reference_window_id(s)
check_window_id
side/direction
hunter/protected
confirmation_timeframe + candle close
reference policy hash
weekly policy hash
```

## signal ID

Canonical JSON → SHA-256. Relative indices مانند D0/K1 identity نیستند.

## dedup layers

1. raw sweep dedup در check window.
2. confirmed event dedup در signal ID.
3. trade entitlement dedup.
4. session quota registry.
5. drawing object registry.

هر layer key مستقل دارد؛ object existence نباید جای ledger را بگیرد.

## ledger dispositions

`OBSERVED`, `CANCELLED_BEFORE_CLOSE`, `CONFIRMED`, `SUPPRESSED_BY_WW`, `SUPPRESSED_BY_QUOTA`, `DRAWN`, `TRADE_PLANNED`, `ORDER_REJECTED`, `ORDER_ACCEPTED`, `REFERENCE_EXHAUSTED`.

## persistence

برای restart، confirmed events، reference exhaustion، quota consumption و open trade lifecycle باید persisted شوند. raw active candidates می‌توانند از M1 reconstruct شوند.

## سطح اختیار این سند

این سند چهار سطح حقیقت را از هم جدا می‌کند:

| سطح | معنی |
|---|---|
| `OWNER_CONFIRMED` | در فایل Word یا درخواست صریح مالک آمده است. |
| `LEGACY_IMPLEMENTED` | در `FP 101.mq5` وجود دارد، حتی اگر قرارداد نهایی نباشد. |
| `ARCHITECTURAL_DERIVATION` | برای ماژولارکردن و حفظ هسته‌های مشترک از منبع استنتاج شده است. |
| `OPEN_DECISION` | قبل از کدنویسی نهایی نیازمند تصمیم مالک است. |

قاعده: رفتار Legacy فقط وقتی canonical است که با Owner Intent و قرارداد این پکیج تعارض نداشته باشد.

## ناوبری

- [[00_EXP0019_MOC|MOC اصلی EXP0019]]
- [[33_AMBIGUITY_AND_DECISION_REGISTER|ثبت ابهام‌ها و تصمیم‌ها]]
- [[34_IMPLEMENTATION_ROADMAP|نقشه پیاده‌سازی]]
- [[35_HANDOFF_TO_CODE|تحویل به کدنویسی]]
