---
title: "26 — قرارداد Inputs و Configuration"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 26 — قرارداد Inputs و Configuration

## گروه‌های input

### Identity/Symbols
- Symbol1, Symbol2.
- Context version/profile.

### Time
- broker UTC offset minutes.
- auto NY DST.
- manual NY offset minutes.
- confirmation timeframe.

### Detection
- enable AL/AN/LN/NA/NL/NN/WW.
- cross-day lookback count/mode.
- historical drawing weeks.
- strict M1 coverage.

### WW
- weekly boundary mode.
- gate enabled.
- no-WW behavior.
- conflict behavior.

### Drawing
- per relation color/label/enabled.
- line width/font.
- session box enable/colors.
- raw audit vs trading view.

### Execution
- runtime mode.
- risk percent default 2.
- reward R default 1.
- one-entry session quota mode.
- spread/deviation/magic.

## validation

- symbols distinct/nonempty.
- lookback bounded.
- timer/process budget bounded.
- risk 0<risk<=configured safety max.
- reward>0.
- live mode requires explicit second gate.

## config hash

تمام behavior-changing inputs در canonical config hash وارد می‌شوند. colors/labels در visual hash جدا هستند تا research signal ID با تغییر رنگ عوض نشود.

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
