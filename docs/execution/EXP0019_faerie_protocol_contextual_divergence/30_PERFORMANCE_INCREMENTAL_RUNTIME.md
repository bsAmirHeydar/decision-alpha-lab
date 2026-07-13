---
title: "30 — Runtime Incremental و Performance"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 30 — Runtime Incremental و Performance

## اصل

History backfill و live incremental update دو pipeline جدا هستند.

## backfill

- یک بار در init یا فرمان operator.
- batch شده بر حسب trading day/week.
- progress/cancel/resume.
- cache reference ranges و event hashes.
- CPU budget per timer pulse.

## live

Triggers:

- new M1 bar: active session/week range update.
- new confirmation bar close: candidate re-evaluation.
- session close: reference freeze.
- weekly boundary: WW rollover.

## ممنوعیت

`ProcessAllSignals()` روی تمام هفته‌ها در هر timer ممنوع است.

## caches

- Window cache.
- Symbol range cache.
- Reference lifecycle registry.
- Candidate registry.
- Drawing registry.
- Quota registry.

## invalidation

cache key باید symbol contract، timeframe source، window UTC bounds، config version و data revision را داشته باشد.

## benchmark profile

پروفایل SET واقعی `100 weeks × 13 N-depth` باید performance acceptance test باشد؛ نه default live processing loop.

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
