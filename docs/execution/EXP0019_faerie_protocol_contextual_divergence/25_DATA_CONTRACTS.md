---
title: "25 — قراردادهای داده"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 25 — قراردادهای داده

## FPWindow

```text
window_id, kind(A/L/N/W), trading_day/week_key,
start_ny, end_ny_exclusive, start_utc, end_utc,
state, source_policy_hash
```

## FPSymbolRange

```text
window_id, symbol, coverage_status, high, low,
high_time_m1, low_time_m1, copied_bars, source_hash
```

## FPReferencePair

```text
relation_code, reference_window_id, symbol1_range, symbol2_range,
side_lifecycle_high, side_lifecycle_low, ready
```

## FPDivergenceEvent

```text
event_id, relation, side, direction, hunter, protected,
reference/check ids, first_sweep_time, confirmation_close,
status, WW disposition, quota disposition, evidence hashes
```

## FPTradePlan

```text
entitlement_id, event_id, trade_symbol, entry, stop, target,
risk_percent, risk_money, volume, geometry_status
```

## closure

تمام enumها closed و versioned هستند. unknown fields در schema implementation باید reject شوند، نه ignore.

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
