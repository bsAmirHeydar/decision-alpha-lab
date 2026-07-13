---
title: "29 — Audit کامل کد Legacy FP101"
tags: [exp0019, faerie-protocol, divergence-context]
status: audit
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 29 — Audit کامل کد Legacy FP101

## نقاط مفید

- سه session window و auto/manual offset در یک نمونه قابل مطالعه‌اند.
- relation descriptor برای شش signal وجود دارد.
- touch-only و closed-bar scan پیاده شده است.
- line immutable و session boxes وجود دارند.
- chart discovery و missing-history tolerance اولیه وجود دارد.

## شکاف‌ها و ریسک‌ها

| شدت | مورد | اثر | قرارداد جایگزین |
|---|---|---|---|
| Critical | reference/range روی `PERIOD_CURRENT` | نتیجه با timeframe عوض می‌شود و مرز 09:30 آلوده می‌شود | M1 exact `[start,end)` |
| Critical | object names با D0/K1 | روز بعد collision و جلوگیری از drawing جدید | absolute event/window IDs |
| High | WW وجود ندارد | 7th relation و weekly gate غایب | weekly provider + gate |
| High | execution وجود ندارد | entry/risk/R/quota غایب | execution adapter جدا |
| High | full rescan هر 5 ثانیه | SET با 100 هفته بسیار سنگین | cache/backfill scheduler |
| High | DST transition در 02:00 UTC | چند ساعت transition غلط | CGT exact 07:00/06:00 UTC |
| High | `LevelAlreadyBroken` hunter را هم مصرف می‌کند | repeated-stage Owner behavior از بین می‌رود | protected-only lifecycle |
| Medium | calendar-day k | weekend باعث کمتر از N session واقعی می‌شود | configurable selector mode |
| Medium | `<= totalDays` | امکان off-by-one در weeks semantics | exact inclusive/exclusive contract |
| Medium | dedup با ObjectFind | drawing و signal authority مخلوط | ledger/registry |
| Medium | sweep time=bar open | exact first touch از بین می‌رود | M1/tick timestamp |
| Medium | charts خودکار باز می‌شوند | side effect و تست غیرvisual | chart service policy |
| Low | active box right edge فراتر از now | visual distortion | min(now, session_end) |

## discrepancy با SET

Lookback=100 و NDepth=13 نشان می‌دهد الگوریتم فعلی در runtime عملی ممکن است میلیون‌ها bar lookup تکراری انجام دهد. این profile باید benchmark fixture باشد.

## نتیجه

FP101 source-of-ideas است، نه implementation base. هیچ copy-paste مستقیم پیشنهاد نمی‌شود؛ فقط رفتارهای owner-confirmed از طریق adapterهای stable core بازسازی می‌شوند.

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
