---
title: "09 — مدل Symbol Pair و نقش Hunter/Protected"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 09 — مدل Symbol Pair و نقش Hunter/Protected

## اصل symbol-local

SPX/NDX یا هر pair دیگر بر اساس سطح قیمت مطلق با هم مقایسه نمی‌شوند. برای یک relation، دو reference هم‌زمان داریم:

```text
reference_A_on_symbol1, reference_A_on_symbol2
```

هر نماد سطح خودش را hunt می‌کند.

## نقش‌ها dynamic هستند

- Symbol1 می‌تواند hunter یا protected باشد.
- Symbol2 می‌تواند hunter یا protected باشد.
- هیچ leader/follower ثابت وجود ندارد.

## high-side

Exactly one high hunt → bearish/SELL context؛ trade candidate=protected.

## low-side

Exactly one low hunt → bullish/BUY context؛ trade candidate=protected.

## paired data readiness

Signal فقط وقتی `data_ready=true` است که reference/check coverage هر دو نماد معتبر باشد. missing یک نماد نباید به‌عنوان «نزدن سطح» تعبیر شود.

## expiry symbols

نمادهای سررسیدی مثل `SP500SEP26`/`NDQ100SEP26` identity مستقل دارند. rollover یا alias mapping باید explicit باشد و eventهای دو قرارداد به‌طور silent به هم متصل نشوند.

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
