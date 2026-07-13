---
title: "28 — برنامه Adapter برای ماژول‌های موجود"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 28 — برنامه Adapter برای ماژول‌های موجود

## فاز compatibility

قبل از استخراج primitive مشترک، golden fixtures EXP0017 روی `CGT/CGR/CGH/CGD/CGX` ثبت می‌شوند. سپس adapterهای FP نوشته می‌شوند بدون تغییر public behavior قدیمی.

## Adapterها

### `FPT_CGTAdapter`
`SCGTTimeSnapshot` را می‌گیرد و A/L/N identities می‌سازد.

### `FPR_CGRWindowAdapter`
arbitrary window را به M1 aggregator می‌دهد؛ enumeration CG قبلی را bypass می‌کند.

### `FPH_CGHAdapter`
paired reference + current/check range را به symbol hunt facts تبدیل می‌کند و first-sweep evidence اضافه می‌کند.

### `FPD_CGDAdapter`
raw exact-one-symbol output را به relation code و FP event material project می‌کند.

### `FPC_CGXClosedCandleAdapter`
confirmation candle را materialize و paired state را در close re-evaluate می‌کند.

### `FPX_CGXExecutionAdapter`
volume/target/quote geometry را reuse می‌کند؛ stop model و quota FP-specific هستند.

## freeze policy

هیچ `if(relation==AL)` داخل فایل‌های EXP0017 اضافه نمی‌شود. اگر primitive عمومی لازم باشد، فایل shared جدید با differential tests ساخته می‌شود.

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
