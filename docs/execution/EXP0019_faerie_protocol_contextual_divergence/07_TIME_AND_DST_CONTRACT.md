---
title: "07 — قرارداد زمان و DST"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 07 — قرارداد زمان و DST

## منبع زمان

تمام policyهای FP با wall-clock نیویورک تعریف می‌شوند. زمان broker فقط transport است.

```text
broker_time -> UTC -> NewYork wall clock -> trading_day/session/week identity
```

## DST canonical

- شروع EDT: دومین یکشنبه مارس، ساعت 07:00 UTC.
- پایان EDT: اولین یکشنبه نوامبر، ساعت 06:00 UTC.
- Auto mode default.
- Manual offset mode برای override عملیاتی.

## reuse

`CCGT_TimeAnatomy::NewYorkOffsetFromUtc` رفتار دقیق transition را دارد و canonical reference فعلی است. تابع Legacy `GetNthSundayUTC(... 02:00)` در ساعات transition دقیق نیست و نباید کپی شود.

## DST در windowهای تاریخی

offset باید برای timestamp خود window محاسبه شود، نه یک offset ثابت «الان». A/L/N یا W که روی transition قرار می‌گیرند ممکن است طول UTC متفاوت ولی طول wall-clock policy ثابت داشته باشند.

## Broker offset

منبع Word `double` offset دارد؛ core موجود integer-hour است. قرارداد هدف باید offset را بر حسب دقیقه نگه دارد:

```text
broker_utc_offset_minutes
manual_ny_utc_offset_minutes
```

این کار brokerهای نیم‌ساعته/ربع‌ساعته را هم بدون تغییر core semantic پوشش می‌دهد.

## failure policy

- offset نامعتبر: init failure.
- timestamp ambiguous/nonexistent: conversion با rule آمریکا و audit flag.
- تاریخ خارج از محدوده terminal: missing-time evidence، نه fallback silent.

## Golden tests

- 2026-03-08 قبل/بعد 07:00 UTC.
- 2026-11-01 قبل/بعد 06:00 UTC.
- A در شب transition.
- historical lookback که از EDT به EST عبور می‌کند.

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
