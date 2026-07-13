---
title: "05 — ماتریس reuse هسته‌های قبلی"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 05 — ماتریس reuse هسته‌های قبلی

## اصل

هسته‌های معتبر قبلی تغییر نمی‌کنند. EXP0019 با adapter و wrapper از آن‌ها استفاده می‌کند. اگر interface فعلی بیش از حد CG-specific باشد، ابتدا compatibility harness نوشته می‌شود و سپس primitive مشترک بدون تغییر رفتار نسخه قبلی استخراج می‌گردد.

## ماتریس

| ماژول موجود | قابلیت قابل reuse | وضعیت | FP adapter/new policy |
|---|---|---|---|
| `CGT_Time.mqh` | DST دقیق آمریکا: 07:00 UTC شروع و 06:00 UTC پایان؛ trading-day 18→17 | Freeze/Reuse | `FPT_SessionCalendar` روی snapshot آن A/L/N می‌سازد. |
| `CGR_ReferenceField.mqh` | M1 coverage، high/low و extreme timestamps | Reuse primitive | `FPR_WindowReferenceAdapter` arbitrary window می‌دهد؛ previous-CG enumeration استفاده نمی‌شود. |
| `CGH_HuntField.mqh` | symbol-local touch predicates و current range | Reuse semantic | `FPH_FirstSweepAdapter` first-touch time و lifecycle را اضافه می‌کند. |
| `CGD_DivergenceField.mqh` | exact-one-symbol high/low asymmetry، hunter/clean | Reuse semantic | `FPD_ContextProjector` relation metadata را attach می‌کند. |
| `CGX_ClosedCandle.mqh` | closed-candle materialization | Reuse مستقیم | `FPC_ConfirmationBoundary` مالکیت window/candle را کنترل می‌کند. |
| `CGX_SignalRegistry.mqh` | one-shot entitlement storage | Reuse pattern | key باید FP absolute identity باشد و day/session quota جداست. |
| `CGX_VolumeModel.mqh` | risk percent equity، broker min/max/step | Reuse مستقیم | default FP=2%. |
| `CGX_TargetModelRiskMultiple.mqh` | R-multiple target | Reuse مستقیم | default FP=1R. |
| `CGX_TradePlanner.mqh` | quote/geometry/plan orchestration | Adapter | stop model جایگزین reference stop می‌شود. |
| `CGV_Drawing.mqh` | object lifecycle، chart lookup، local-symbol drawing | Reuse primitives | `FPV_RelationLineRenderer` و `FPV_SessionBoxRenderer` جدید. |
| `CGV_Ledger.mqh` | visual audit ledger pattern | Reuse pattern | FP event/disposition fields افزوده می‌شود. |

## مواردی که نباید reuse شوند

- EXP0017 cycle-group registry و previous-cycle enumeration.
- STC/M/W signal taxonomy.
- confirmation-candle stop model فعلی raw execution.
- D0/K object naming در FP101.
- timer full-rescan loop.

## Compatibility rule

هر extraction از core قبلی باید golden vectors قبلی EXP0017 را بدون تغییر hash/semantic پاس کند. FP feature نباید به‌صورت patch داخل فایل core قدیمی اضافه شود.

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
