---
title: "21 — قرارداد Entry، Risk، Stop و Target"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 21 — قرارداد Entry، Risk، Stop و Target

## entry

- بعد از confirmation candle close.
- روی protected/clean symbol.
- market entry در profile اجرایی.

## stop

```text
BUY  -> protected reference low
SELL -> protected reference high
```

این stop model با `CGX_STOP_BEHIND_CONFIRMATION_CANDLE` متفاوت است و باید ماژول جدید `FPX_ProtectedReferenceStopModel` باشد.

## target

R-multiple input؛ default `1.0R`.

```text
BUY TP  = entry + R * (entry - stop)
SELL TP = entry - R * (stop - entry)
```

`CGX_TargetModelRiskMultiple` قابل reuse است.

## risk

Risk-percent-equity input؛ default `2.0%`. volume باید بزرگ‌ترین volume مجاز باشد که planned loss از budget عبور نکند. `CGX_VolumeModel` قابل reuse است.

## geometry failures

- stop در سمت غلط entry.
- stop distance صفر/منفی.
- broker stops level.
- tick value/size نامعتبر.
- minimum lot بیش از risk budget.

همه fail-closed و ledgered هستند.

## authority

این سند contract است، نه فعال‌سازی live. implementation باید modes research/drawing/paper/live-gated داشته باشد.

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
