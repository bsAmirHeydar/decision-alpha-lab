---
title: "27 — معماری ماژولار MQL5"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 27 — معماری ماژولار MQL5

## EA host

فایل Expert فقط orchestration، inputs و lifecycle callbacks دارد. هیچ business rule مستقیم در `OnTick/OnTimer` نوشته نمی‌شود.

## پکیج پیشنهادی

```text
mql5/Include/IntermarketDivergenceExecution/FP/
  FPT_Types.mqh
  FPT_SessionCalendar.mqh
  FPR_RelationRegistry.mqh
  FPR_ReferenceSelector.mqh
  FPF_ReferenceLifecycle.mqh
  FPH_FirstSweepField.mqh
  FPD_ContextProjector.mqh
  FPC_ConfirmationEngine.mqh
  FPW_WeeklyContext.mqh
  FPG_WeeklyDirectionGate.mqh
  FPE_SessionQuota.mqh
  FPV_Drawing.mqh
  FPL_Ledger.mqh
  FPB_BackfillScheduler.mqh
  Execution/
    FPX_StopModelReference.mqh
    FPX_TradePlannerAdapter.mqh
    FPX_RuntimeRouter.mqh
```

## dependency direction

```text
Shared cores <- FP adapters <- FP policy <- host
Execution depends on confirmed policy output only.
```

## ممنوع

- circular include.
- global mutable arrays as authority.
- recompute reference in execution.
- object names as dedup state.
- full history scan inside every timer pulse.

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
