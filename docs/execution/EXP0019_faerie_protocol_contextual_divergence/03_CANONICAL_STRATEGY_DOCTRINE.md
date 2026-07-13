---
title: "03 — دکترین canonical استراتژی"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 03 — دکترین canonical استراتژی

## دکترین‌های ثابت

1. **واگرایی اختلاف رفتار بین دو بازار مرتبط است؛ نه مقایسه قیمت مطلق دو بازار.**
2. **هر نماد فقط سطح خودش را hunt می‌کند.**
3. **Touch/Equality/Cross همگی hunt هستند.**
4. **Candidate intrabar ممکن است؛ confirmation فقط روی closed candle است.**
5. **Hunter سطح خودش را زده؛ Protected سطح متناظر خودش را حفظ کرده است.**
6. **Core detector هیچ دانشی از A/L/N/WW ندارد.**
7. **Faerie context فقط window، relation، eligibility و gating را تعریف می‌کند.**
8. **Raw detections حتی اگر WW یا quota آن‌ها را suppress کند باید در ledger بمانند.**
9. **Reference protected با touch نماد protected برای آینده exhausted می‌شود؛ confirmed history حذف نمی‌شود.**
10. **Execution از detection و drawing جداست.**
11. **هر رفتار identity-bearing باید در event ID و config hash حاضر باشد.**
12. **مفقودی دیتا مساوی no-signal نیست؛ وضعیت مستقل `MISSING_DATA` است.**

## سه سطح خروجی

| سطح | خروجی | اجازه معامله |
|---|---|---|
| Observation | range/reference/hunt facts | خیر |
| Context Signal | confirmed divergence + FP relation | خیر |
| Trade Entitlement | WW-aligned + quota + risk/geometry pass | فقط در execution profile |

## عدم اختلاط Context و Quality

Faerie Protocol در این سند context تعریف می‌کند، نه اینکه ادعا کند هر FP signal edge دارد. ranking، statistics و promotion باید پایین‌دست و مستقل باشند.

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
