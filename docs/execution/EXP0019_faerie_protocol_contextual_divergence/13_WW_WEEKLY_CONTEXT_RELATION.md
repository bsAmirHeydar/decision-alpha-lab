---
title: "13 — رابطه هفتگی WW"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 13 — رابطه هفتگی WW

## Owner Intent

WW یعنی بین weekly candle در حال تشکیل و weekly candle قبل divergence وجود داشته باشد. WW علاوه بر signal بودن، جهت relationهای دیگر همان هفته را gate می‌کند.

## چیزی که هنوز مبهم است

- W بر اساس MetaTrader `PERIOD_W1` است یا New York trading week؟
- WW خودش tradeable است یا فقط gate؟
- confirmation boundary weekly چیست؟ chart timeframe close یا week close؟

## baseline معماری

WW با همان shared divergence core ساخته می‌شود، اما window provider مستقل دارد. توصیه:

```text
New York trading week: Sunday 18:00 NY -> Friday 17:00 NY
previous completed week -> current active week
```

این انتخاب broker-independent است ولی قبل از coding باید مالک تأیید کند.

## weekly reference lifecycle

- previous W باید complete باشد.
- current W active range از M1/timeseries ساخته می‌شود.
- one-sided touch می‌تواند `BULLISH_WEEKLY_CONTEXT` یا `BEARISH_WEEKLY_CONTEXT` بدهد.
- symmetric touch context را neutral/invalid می‌کند طبق confirmation rule.

## جداسازی

WW raw event در detector تولید می‌شود؛ اثر آن بر lower relations فقط در `FPWeeklyDirectionGate` اعمال می‌شود. core divergence از WW خبر ندارد.

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
