---
title: "33 — Ambiguity و Decision Register"
tags: [exp0019, faerie-protocol, divergence-context]
status: decision-register
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 33 — Ambiguity و Decision Register

## تصمیم‌های باز

| ID | موضوع | گزینه‌ها | توصیه baseline | Blocking |
|---|---|---|---|---|
| FP-DEC-001 | WW boundary | broker W1 / NY trading week | NY trading week | بله برای WW code |
| FP-DEC-002 | WW tradeability | gate-only / signal+trade | gate-only ابتدا | بله execution WW |
| FP-DEC-003 | WW no-context | allow both / block all | allow both | بله policy |
| FP-DEC-004 | WW conflict both sides | block / last-event / both | block and audit | بله policy |
| FP-DEC-005 | N lookback counting | calendar / available sessions | available sessions | بله selector |
| FP-DEC-006 | session quota scope | pair / symbol / direction / relation | pair-global | بله execution |
| FP-DEC-007 | quota consumption | plan / order attempt / fill | accepted fill | بله execution |
| FP-DEC-008 | boundary-cross confirmation candle | event-time / strict session | event-time ownership | بله confirmation |
| FP-DEC-009 | suppressed drawing | hide / draw muted / raw mode only | configurable; trading view hide | خیر detection |
| FP-DEC-010 | historical confirmed invalidation visuals | immutable / remove | immutable (owner-confirmed) | بسته |
| FP-DEC-011 | repeated same reference stages | allow until protected touch / first-ever only | allow per check window | نیاز تأیید نهایی |
| FP-DEC-012 | spread adjustment on sell stop | none / add spread | none تا دستور صریح | execution |

## قاعده

هیچ گزینه پیشنهادی تا owner confirmation به `OWNER_CONFIRMED` ارتقا نمی‌یابد. Code باید decision IDs/version را در config/manifest ثبت کند.

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
