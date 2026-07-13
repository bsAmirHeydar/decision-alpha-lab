---
title: "31 — Data Gaps، Expiry و Weekend"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 31 — Data Gaps، Expiry و Weekend

## اصل fail-closed

No data ≠ not hunted. هر window status دارد:

- READY_COMPLETE
- PARTIAL_COVERAGE
- NO_HISTORY
- SYMBOL_UNAVAILABLE
- CONTRACT_NOT_LISTED
- WEEKEND_NO_SESSION

## expiry

اگر قرارداد فقط یک روز history دارد، فقط referenceهای معتبر همان محدوده تولید می‌شوند. engine نباید array/index error بدهد و نباید missing را synthetic fill کند.

## weekend

A Sunday open و weekends broker-specific است. Calendar باید NY policy بسازد؛ series layer گزارش می‌دهد داده واقعی وجود دارد یا نه.

## lookback counting

هر دو semantics باید صریح باشند:

- calendar depth.
- available-session count.

نتیجه و event ID بدون mode قابل مقایسه نیست.

## pair asymmetry in data

اگر یک symbol history دارد و دیگری ندارد، relation status `PAIR_DATA_INCOMPLETE` است و هیچ divergence ساخته نمی‌شود.

## restart/data revision

اگر broker historical bars را اصلاح کرد، source hash تغییر می‌کند؛ cached artifact stale و superseding audit لازم است.

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
