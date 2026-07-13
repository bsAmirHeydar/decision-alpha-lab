---
title: "10 — Taxonomy و Relation Registry هفت‌گانه"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 10 — Taxonomy و Relation Registry هفت‌گانه

## Registry canonical

| relation | reference selector | check selector | scope |
|---|---|---|---|
| AL | A همین trading day | L همین trading day | same-day |
| AN | A همین trading day | N همین trading day | same-day |
| LN | L همین trading day | N همین trading day | same-day |
| NA | N روزهای قبل | A روز جاری | cross-day |
| NL | N روزهای قبل | L روز جاری | cross-day |
| NN | N روزهای قبل | N روز جاری | cross-day |
| WW | W قبلی | W جاری | weekly context |

## descriptor پیشنهادی

```cpp
struct FPRelationDef {
  relation_code;
  reference_window_kind;
  check_window_kind;
  reference_scope;
  max_reference_depth;
  enable_detection;
  enable_drawing;
  enable_execution;
  color;
  label;
};
```

## invariants

- relation order در registry authority نیست؛ code string authority است.
- هر relation input مستقل دارد.
- WW در detector registry است ولی policy role آن می‌تواند `GATE_ONLY` باشد.
- یک confirmation candle می‌تواند چند relation مستقل تولید کند.
- buy/sell sideها eventهای جدا هستند.

## legacy gap

FP101 فقط شش relation دارد و `SIGNAL_COUNT=6`. افزودن WW با افزایش array کافی نیست؛ weekly window provider و directional gate لازم است.

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
