---
title: "34 — نقشه پیاده‌سازی مرحله‌ای"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 34 — نقشه پیاده‌سازی مرحله‌ای

## Phase 00 — Doctrine Freeze

- تصمیم‌های blocking را ببند.
- relation registry/config schema freeze.
- source traceability sign-off.

## Phase 01 — Compatibility Harness

- golden vectors CGT/CGR/CGH/CGD/CGX.
- ثابت‌بودن هسته‌های EXP0017.

## Phase 02 — FP Types and Registry

- window/relation/event/lifecycle types.
- seven descriptors.

## Phase 03 — Time and Session Calendar

- exact NY conversion.
- A/L/N identities and tests.

## Phase 04 — Window Range and References

- M1 aggregator adapter.
- same-day/cross-day selectors.
- data gap statuses.

## Phase 05 — Hunt and Lifecycle

- first sweep.
- protected-only exhaustion.
- repeated-stage tests.

## Phase 06 — Divergence and Confirmation

- raw candidates.
- close projection.
- cancellation-before-close.

## Phase 07 — WW

- weekly provider.
- weekly raw divergence.
- direction gate.

## Phase 08 — Ledger and Identity

- absolute IDs.
- persistence/restart.
- dedup layers.

## Phase 09 — Visuals

- hunter relation line.
- labels and boxes.
- multi-chart service.

## Phase 10 — Backfill/Performance

- cache.
- 100-week benchmark.
- incremental scheduler.

## Phase 11 — Paper Execution

- protected reference stop.
- 1R default, 2% default.
- session quota.

## Phase 12 — Live Gate

- broker geometry.
- recovery.
- explicit operator authorization.

هر phase patch مستقل، testable و rollbackable است.

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
