---
title: "32 — Test Strategy و Golden Cases"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 32 — Test Strategy و Golden Cases

## لایه‌های تست

1. Time/DST unit tests.
2. Window/session identity.
3. M1 aggregation and coverage.
4. Touch and first sweep.
5. Reference lifecycle.
6. Relation matrix.
7. Closed-candle confirmation.
8. WW gate.
9. quota/entitlement.
10. drawing identity.
11. risk/geometry.
12. restart/cache/dedup.
13. performance/backfill.

## Golden cases

### G01 AL sell
A references ready؛ Symbol1 high hunts در L؛ Symbol2 نه؛ close حفظ → SELL, hunter1/protected2.

### G02 AL transient cancelled
Symbol1 first hunts؛ قبل از close Symbol2 هم hunts → CANCELLED_BEFORE_CLOSE، no final line.

### G03 same candle multi-relation
AN و LN sell در یک close → دو event ID و دو line.

### G04 repeated-stage allowed
N reference؛ hunter در A event؛ protected intact؛ hunter در L event جدید → دو event. سپس protected touch → future NN blocked.

### G05 missing protected data
hunter data ready، protected missing → no divergence، `PAIR_DATA_INCOMPLETE`.

### G06 WW bullish gate
lower sell confirmed → raw ledger + `SUPPRESSED_BY_WW`؛ lower buy eligible.

### G07 session quota
دو eligible event در N → deterministic first consumes quota؛ second `SUPPRESSED_BY_QUOTA`.

### G08 object identity next day
D0 equivalent events دو روز متفاوت → object IDs متفاوت.

### G09 DST transition
A/L windows exact across March/November transition.

### G10 timeframe invariance
M5/H1 host همان M1 reference/hunt facts را تولید کنند؛ فقط confirmation times متفاوت.

## property tests

- symmetric paired input under symbol swap swaps hunter/protected but keeps direction.
- both hunt => no divergence.
- neither hunt => no divergence.
- identity changes on behavior policy change.

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
