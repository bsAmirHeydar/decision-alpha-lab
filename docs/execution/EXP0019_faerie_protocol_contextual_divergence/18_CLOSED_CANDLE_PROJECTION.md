---
title: "18 — Projection به Closed Candle"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 18 — Projection به Closed Candle

## confirmation timeframe

Timeframe چارت/ورودی فقط boundary confirmation است؛ reference/hunt range با M1 مستقل از آن ساخته می‌شود.

## projection rule

برای هر raw candidate، اولین closed candle که `candidate_first_seen_time` داخل آن است، confirmation candle است. در close آن، paired state دوباره ارزیابی می‌شود.

## session boundary crossing

اگر confirmation candle از end session عبور کند، دو policy ممکن است:

- `EVENT_TIME_OWNERSHIP`: event متعلق به session زمان first sweep است و در close بعدی confirm می‌شود.
- `STRICT_SESSION_CLOSE`: candle باید داخل session بسته شود.

Owner فقط candle close را قطعی کرده، نه boundary-cross rule. baseline پیشنهادی `EVENT_TIME_OWNERSHIP` است تا H1 روی 09:30 قابل استفاده باشد؛ تصمیم باید ثبت شود.

## closed-bar source

`CGX_ClosedCandleProvider` برای materialization قابل reuse است، اما candidate state باید از paired M1 field در close گرفته شود.

## restart

pending candidates باید با deterministic reconstruction از M1 + last processed close بازیابی شوند؛ object existence authority نیست.

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
