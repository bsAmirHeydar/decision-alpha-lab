---
title: "37 — Limits، Non-Goals و Governance"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 37 — Limits، Non-Goals و Governance

## non-goals این فاز

- کدنویسی EA.
- ادعای edge آماری.
- بهینه‌سازی parameters.
- live trading.
- ادغام FP با EXP0017 core.
- بازنویسی هسته‌های تاییدشده.

## governance

- Context version immutable پس از استفاده در dataset/backtest.
- rule change → نسخه جدید، نه mutation silent.
- raw، confirmed، policy-suppressed و traded counts جدا گزارش شوند.
- drawing outcome authority نیست.
- open decisions در code comment حل نمی‌شوند؛ در register بسته می‌شوند.

## residual risks

- تعریف دقیق W.
- quota scope.
- confirmation candle در session boundary.
- history revision broker.
- symbol rollover/contract mapping.
- spread/stop geometry live.

## next action

مالک Decision Register را مرور و موارد blocking را تأیید می‌کند؛ سپس Phase 01 implementation آغاز می‌شود.

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
