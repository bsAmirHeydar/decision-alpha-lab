---
title: "01 — موجودی کامل منبع"
tags: [exp0019, faerie-protocol, divergence-context]
status: source-record
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 01 — موجودی کامل منبع

## فایل‌های ورودی

| فایل | نقش | SHA-256 |
|---|---|---|
| `05_Faerie Protocol_2.docx` | توضیحات مالک، جدول زمانی و تصمیم‌های تکمیلی | `acb67952584d431fe5d9bfd64ad704259a609304c2c4c18c0710d3321469390c` |
| `FP 101.mq5` | نمونه Legacy رسم و تشخیص شش رابطه | `672e0f3cca5edf3db573dcc200a5f8295fe92f7b50defd82c69eaaded22c7589` |
| `fp101.set` | پروفایل واقعی استفاده‌شده با نمادهای سررسیدی و lookback بزرگ | `628e5acb92e94609f857e587fce9cc56d42ce141997735c737ad914c137645a3` |

## محتوای Word

- 128 پاراگراف، 1 جدول، 3 تصویر داخلی، 7 صفحه رندرشده.
- سه سشن A/L/N.
- هفت رابطه AL/AN/LN/NA/NL/NN/WW.
- تعریف touch hunt، candle-close confirmation، drawing، boxes، lookback، DST، reference consumption و execution.

## محتوای EA

- 752 خط MQL5.
- 40 input.
- 31 تابع top-level.
- 6 relation؛ WW غایب.
- drawing-only؛ execution غایب.
- پردازش مبتنی بر `PERIOD_CURRENT`.

## محتوای SET

پروفایل واقعی با این تفاوت‌ها نسبت به default کد اجرا شده است:

| فیلد | default کد | SET |
|---|---:|---:|
| Symbol1 | SPXUSD | SP500SEP26 |
| Symbol2 | NDXUSD | NDQ100SEP26 |
| LookbackWeeks | 2 | 100 |
| NLookbackDays | 7 | 13 |
| AL label | AL | A |

این تفاوت‌ها نشان می‌دهد معماری باید symbol-contract expiry، backfill سنگین و label customization را مستقل مدیریت کند.

## خروجی‌های audit این پکیج

- [[source_audit/OWNER_INTENT_TRANSCRIPT_FA]]
- `source_audit/FP101_INPUT_INVENTORY.csv`
- `source_audit/FP101_FUNCTION_INVENTORY.csv`
- `source_audit/FP101_SET_NORMALIZED.ini`
- `source_audit/SOURCE_TO_RULE_TRACEABILITY.csv`
- `source_audit/SOURCE_HASHES.sha256`

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
