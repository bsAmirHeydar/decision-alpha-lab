---
title: "22 — قرارداد Drawing و Session Boxes"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 22 — قرارداد Drawing و Session Boxes

## divergence line

- فقط یک `OBJ_TREND` ساده به‌عنوان main semantic.
- روی chart hunter symbol.
- anchor 1: exact reference extreme timestamp/price hunter.
- anchor 2: confirmation candle extreme/time hunter؛ high برای sell، low برای buy.
- label relation code در midpoint.
- color/width/font configurable.

## simultaneous events

تمام relationها و هر دو جهت که confirmed شوند line مستقل دارند؛ object ID collision ممنوع است.

## immutability

confirmed line پس از رسم جابجا یا حذف نمی‌شود مگر operator cleanup صریح. cancelled-before-close line نهایی ندارد.

## session boxes

برای هر symbol و trading day:

- A box high/low از M1 A.
- L box high/low از M1 L.
- N box high/low از M1 N.
- active box incremental update؛ complete box freeze.
- fill color مستقل.

## object names

```text
FP19|DIV|<event_id>
FP19|LBL|<event_id>
FP19|BOX|<symbol_hash>|<trading_day>|<session>
```

نام Legacy `D0/K1` ممنوع است چون روز بعد collision می‌سازد.

## chart management

Chart discovery/opening یک service جداست. drawing failure signal authority را تغییر نمی‌دهد.

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
