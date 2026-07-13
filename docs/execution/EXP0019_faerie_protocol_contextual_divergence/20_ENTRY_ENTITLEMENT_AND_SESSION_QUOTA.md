---
title: "20 — Entry Entitlement و سهمیه سشن"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 20 — Entry Entitlement و سهمیه سشن

## Owner Intent

در هر A، L و N فقط یک ورود انجام شود. این محدودیت نباید detection یا drawing raw را حذف کند.

## entitlement flow

```text
Confirmed -> WW aligned -> session identified -> quota available
-> risk/geometry valid -> entitlement consumed -> order attempt
```

## session quota key پیشنهادی

```text
context_version + trading_day_key + pair_id + session_code
```

این baseline یعنی یک ورود global برای pair در هر session. Scopeهای ممکن دیگر:

- per trade symbol
- per direction
- per relation

متن منبع scope دقیق را مشخص نکرده؛ Decision Register باز است.

## consumption moment

پیشنهاد: quota فقط پس از accepted order/paper fill مصرف شود؛ rejected geometry یا missing quote quota را مصرف نکند. برای جلوگیری از retry duplicate، entitlement event one-shot جداست.

## concurrency

چند signal همزمان باید deterministic priority داشته باشند. هیچ priority owner-confirmed نیست. baseline research: earliest confirmation time، سپس relation registry order فقط به‌عنوان tie-break versioned.

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
