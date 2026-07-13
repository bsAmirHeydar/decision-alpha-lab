---
title: "15 — قرارداد Hunt، Touch و First Sweep"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 15 — قرارداد Hunt، Touch و First Sweep

## predicate

```text
high_hunt = observed_high >= reference_high
low_hunt  = observed_low  <= reference_low
```

Tolerance baseline=0. هر tolerance آینده باید versioned policy باشد.

## first sweep

اولین M1/tick timestamp که predicate را برقرار می‌کند، برای event key ثبت می‌شود. sweep time باید actual observation time باشد، نه فقط open time confirmation candle.

## same-candle semantics

Owner گفته اگر intrabar divergence بود ولی تا close هر دو نماد سطح را زدند، signal نمایش داده نشود. بنابراین order داخل همان confirmation candle برای validity نهایی مهم نیست؛ state در close authority است. first-sweep time برای audit و drawing باقی می‌ماند.

## duplicate suppression

First sweep uniqueness در سطح زیر است:

```text
reference_id + check_window_id + side + hunter_symbol
```

Touchهای بعدی همان event duplicate هستند. reference می‌تواند در check window بعدی event جدید بدهد اگر protected level هنوز intact باشد.

## missing data

عدم مشاهده hunt فقط وقتی `NOT_HUNTED` است که coverage معتبر باشد؛ در غیر این صورت `UNKNOWN_MISSING_DATA` است.

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
