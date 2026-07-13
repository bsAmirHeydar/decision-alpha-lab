---
title: "36 — Traceability Matrix"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 36 — Traceability Matrix

## مسیر traceability

```text
Owner paragraph / Legacy line
  -> normalized rule ID
  -> canonical document section
  -> future contract field/module
  -> test case
  -> runtime ledger evidence
```

## نمونه‌ها

| Rule | Source | Module | Test |
|---|---|---|---|
| FP-R-TIME-001 A/L/N bounds | P006-P008 | FPT_SessionCalendar | G09 |
| FP-R-HUNT-001 touch-only | P024-P028 | shared HuntCore | G01/G02 |
| FP-R-CONF-001 closed candle | P056-P060 | FPC_ConfirmationEngine | G02 |
| FP-R-LIFE-001 protected exhaustion | P115 | FPF_ReferenceLifecycle | G04 |
| FP-R-WW-001 weekly direction gate | P123 | FPW/FPG | G06 |
| FP-R-EXEC-001 protected entry | P121-P122 | FPX planner | execution tests |
| FP-R-RISK-001 2%/1R | P123 | volume/target adapter | geometry tests |

جدول کامل machine-readable در `source_audit/SOURCE_TO_RULE_TRACEABILITY.csv` است.

## change control

هر تغییر rule باید trace row، affected docs، module، tests و context version را به‌روزرسانی کند. تغییر بدون traceability ناقص است.

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
