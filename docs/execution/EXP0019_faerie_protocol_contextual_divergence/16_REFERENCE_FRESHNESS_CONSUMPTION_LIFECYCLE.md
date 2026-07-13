---
title: "16 — Freshness، Consumption و Lifecycle سطح"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 16 — Freshness، Consumption و Lifecycle سطح

## اصل Owner

سطح وقتی برای آینده از کار می‌افتد که protected symbol سطح متناظر خودش را hunt کند. confirmed line گذشته حذف نمی‌شود.

## دو lifecycle جدا

### Reference-side lifecycle

```text
UNBUILT -> READY_INTACT -> EXHAUSTED_BY_PROTECTED_TOUCH -> EXPIRED_BY_SCOPE
```

### Event lifecycle

```text
OBSERVING -> RAW_ASYMMETRY -> CONFIRMED
                         \-> CANCELLED_BEFORE_CLOSE
CONFIRMED -> ARCHIVED (immutable evidence)
```

## hunter touch مصرف جهانی نیست

مطابق توضیح مالک، اگر protected هنوز protected بماند، همان reference در stage دیگری می‌تواند divergence جدید بسازد. بنابراین touch hunter فقط event فعلی را می‌سازد و reference pair را globally exhaust نمی‌کند.

## تعارض Legacy

FP101 در `LevelAlreadyBroken` هم hunter و هم protected را قبل از check window بررسی و هرکدام touch شده باشد reference را رد می‌کند. این با repeated-stage interpretation سازگار نیست و canonical نیست.

## side-specificity

high و low lifecycle مستقل‌اند. touch high protected نباید low reference همان window را خودکار exhaust کند.

## evidence

هر transition باید timestamp، symbol، side، source bar/tick، previous state و reason code داشته باشد.

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
