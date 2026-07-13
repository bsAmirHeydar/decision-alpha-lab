---
title: "35 — Handoff به کدنویسی"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 35 — Handoff به کدنویسی

## ورودی لازم برای شروع

- Decision IDs blocking بسته شده باشند.
- relation registry v1 freeze.
- source hashes و traceability موجود.
- shared-core compatibility tests سبز.

## اولین patch کد

Scope فقط:

1. `FPT_Types.mqh`
2. `FPT_SessionCalendar.mqh`
3. `FPR_RelationRegistry.mqh`
4. diagnostic EA بدون detection/trade.
5. tests برای DST/A/L/N/registry.

هیچ drawing یا order در patch اول نیست.

## Definition of Done documentation-to-code

- هر struct field به سند data contract لینک دارد.
- هر rule test ID دارد.
- هیچ behavior silent default ندارد.
- event identity absolute است.
- MetaEditor compile log واقعی موجود است.
- existing EXP0017 tests regression ندارند.

## ممنوعیت شروع زودهنگام

WW و quota قبل از بستن Decision Register کدنویسی نشوند. Legacy FP101 نباید فایل پایه implementation باشد.

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
