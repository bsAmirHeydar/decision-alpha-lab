---
title: "06 — واژه‌نامه canonical"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 06 — واژه‌نامه canonical

## واژه‌ها

| واژه | تعریف دقیق |
|---|---|
| Trading Day | بازه 18:00 NY تا 17:00 NY روز بعد. |
| Session A | 18:00:00 تا 03:59:59 NY. |
| Session L | 04:00:00 تا 09:29:59 NY. |
| Session N | 09:30:00 تا 16:59:59 NY. |
| Reference Window | بازه کامل‌شده‌ای که high/low symbol-local می‌سازد. |
| Check Window | بازه‌ای که hunt در آن مشاهده می‌شود. |
| Relation | جفت policy شده reference/check مثل AL یا NN. |
| Hunt | لمس یا عبور high/low مرجع همان نماد. |
| First Sweep | اولین timestamp معتبر hunt برای event key مشخص. |
| Hunter | نمادی که سطح خودش را hunt کرده است. |
| Protected/Clean | نمادی که سطح متناظر خودش را حفظ کرده است. |
| Raw Divergence | exact-one-symbol hunt قبل از close. |
| Confirmed Divergence | raw divergence که در boundary کندل بسته هنوز برقرار است. |
| Cancelled Before Close | intrabar asymmetry که تا close symmetric شده است. |
| Reference Exhaustion | protected symbol سطح خودش را لمس کرده و مرجع برای eventهای آینده بسته شده است. |
| WW Context | رابطه current week با previous week برای direction gating. |
| Trade Entitlement | مجوز one-shot پس از context gate و quota. |
| Session Quota | ظرفیت ورود A/L/N؛ مستقل از تعداد raw signals. |
| Immutable Drawing | artifact confirmed که بعداً با invalidation تاریخی حذف نمی‌شود. |

## نام‌گذاری relation

قاعده canonical:

```text
<ReferenceWindowCode><CheckWindowCode>
```

پس `AL` یعنی A reference → L check و `NA` یعنی historical N reference → current A check.

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
