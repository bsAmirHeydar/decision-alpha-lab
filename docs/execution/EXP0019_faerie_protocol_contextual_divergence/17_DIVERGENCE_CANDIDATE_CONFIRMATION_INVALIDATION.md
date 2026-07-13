---
title: "17 — Candidate، Confirmation و Invalidation"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 17 — Candidate، Confirmation و Invalidation

## raw candidate

در active check window، exact-one-symbol hunt یک raw candidate می‌سازد. این candidate قابل نمایش debug است ولی signal نهایی نیست.

## confirmation

در close اولین confirmation candle که candidate را مشاهده کرده است:

- hunter side هنوز hunted باشد.
- protected side هنوز not-hunted و data-ready باشد.
- relation/reference/check identity معتبر باشد.
- candidate به `CONFIRMED` تبدیل شود.

اگر protected تا close hunt کند، `CANCELLED_BEFORE_CLOSE` ثبت می‌شود و drawing نهایی ساخته نمی‌شود.

## بعد از confirmation

Touch بعدی protected:

- reference را برای eventهای آینده exhaust می‌کند.
- confirmed event و line قبلی را حذف نمی‌کند.
- ledger یک post-confirmation lifecycle transition ثبت می‌کند.

## multiple candidates

Buy و sell یا چند relation در یک candle مستقل ثبت می‌شوند. conflict suppression فقط policy layer است، نه deletion core.

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
