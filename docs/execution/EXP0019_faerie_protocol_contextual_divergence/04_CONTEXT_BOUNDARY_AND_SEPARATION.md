---
title: "04 — مرز Context و جداسازی از واگرایی‌های دیگر"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 04 — مرز Context و جداسازی از واگرایی‌های دیگر

## مسئله

چند خانواده واگرایی در ریپو وجود دارد: EXP0015 time divergence، EXP0016 STC/SMT، EXP0017 Cycle Group و EXP0018 Daye. اگر A/L/N و WW در core مشترک نوشته شوند، core به یک استراتژی خاص آلوده می‌شود و reuse واقعی از بین می‌رود.

## مرز پیشنهادی

```text
DivergenceCore
  input: paired symbol-local references + paired observations
  output: hunter/protected/raw direction

FPContext
  input: trading day/session/relationship/history/week policy
  output: eligible reference-check pairs + context tags

FPPolicy
  input: confirmed FP events + WW + quota
  output: visible/tradeable/suppressed disposition
```

## چیزهایی که فقط FP هستند

- نام و مرز A/L/N.
- relation registry هفت‌گانه.
- N historical selector.
- WW weekly gate.
- session boxes.
- one-entry-per-session.
- FP-specific reference lifecycle interpretation.

## چیزهایی که مشترک می‌مانند

- NY time conversion primitive.
- symbol-local M1 aggregation.
- touch hunt predicate.
- exact-one-symbol asymmetry.
- closed-candle projection.
- signal/event ID.
- ledger/dedup.
- risk-capped volume.

## ممنوعیت coupling

- `DivergenceCore` نباید switch روی `AL` یا `NN` داشته باشد.
- `FPContext` نباید order ارسال کند.
- `FPExecution` نباید reference دوباره محاسبه کند.
- visualization نباید authority signal باشد.

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
