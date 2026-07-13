---
title: "14 — قرارداد Reference Field"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 14 — قرارداد Reference Field

## reference object

هر reference برای هر نماد باید شامل این‌ها باشد:

```text
reference_id, context_version, relation_code, window_id,
symbol, side, high, low, high_time_m1, low_time_m1,
start_utc, end_utc, coverage_status, source_hash
```

## aggregation

- source timeframe canonical = M1.
- high=max high؛ low=min low در `[start,end)`.
- exact extreme timestamp ذخیره شود.
- incomplete coverage status مستقل است.

## چرا PERIOD_CURRENT ممنوع است؟

H1 bar که 09:00 باز شده، بخشی از L و N را در خود دارد. استفاده از high/low آن برای window 04:00–09:30 boundary leakage ایجاد می‌کند. FP101 به `PERIOD_CURRENT` وابسته است و نتیجه با timeframe چارت عوض می‌شود؛ canonical باید timeframe-invariant باشد.

## reference pair

دو نماد باید یک logical window identity داشته باشند ولی price fields مستقل‌اند. ready pair فقط وقتی true است که coverage هر دو side معتبر باشد.

## cache

reference کامل‌شده immutable و content-addressed است. active check range mutable است ولی با sequence/version کنترل می‌شود.

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
