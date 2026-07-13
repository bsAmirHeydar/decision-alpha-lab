---
title: "08 — تقویم روز معاملاتی و سشن‌های A/L/N"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 08 — تقویم روز معاملاتی و سشن‌های A/L/N

## روز معاملاتی

```text
start = 18:00:00 NY
end_exclusive = 17:00:00 NY next calendar day
length = 23 wall-clock hours
```

بازه 17:00 تا 17:59:59 خارج از active field است.

## سشن‌ها

| کد | start NY | end exclusive NY | مدت |
|---|---|---|---:|
| A | 18:00 | 04:00 روز بعد | 600 دقیقه |
| L | 04:00 | 09:30 | 330 دقیقه |
| N | 09:30 | 17:00 | 450 دقیقه |

مجموع دقیقاً 1380 دقیقه است؛ overlap و gap ندارند.

## identity

```text
session_id = hash(context_version, trading_day_key, session_code, start_utc, end_utc)
```

`trading_day_key` باید تاریخ شروع A در New York باشد، نه broker date.

## ownership

- bar با open time داخل session لزوماً تمام range session نیست.
- reference و box از M1 با `[start,end)` ساخته می‌شوند.
- confirmation candle ممکن است boundary را قطع کند؛ rule آن در سند 18 است.

## state

`UPCOMING -> ACTIVE -> COMPLETE -> ARCHIVED`

فقط COMPLETE می‌تواند reference same-day باشد. ACTIVE فقط check observation تولید می‌کند.

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
