---
id: EXP0018-DESIGN-V2-INDEX
title: "EXP0018 Implementation Design v2 — Index"
type: moc
status: active
project: EXP0018
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - daye-trader
  - implementation-design
---

# EXP0018 Implementation Design v2

این شاخه نقشه مهندسی کامل برای تبدیل دکترین Daye/Quarterly Theory به سیستم deterministic، replayable، visual-only و بدون اختیار معامله است.

## Evidence packages ساخته‌شده

- [[CG_EXP0018_PHASE00_DOCTRINE_FREEZE_MOC|P00 Doctrine Freeze v2]]
- [[CG_EXP0018_PHASE01_TIME_KERNEL_MOC|P01 New York Time Kernel v2]]
- [[CG_EXP0018_PHASE02_MULTI_SYMBOL_DATA_SYNC_MOC|P02 Multi-Symbol Data Sync v2]]
- [[CG_EXP0018_PHASE03_PERIOD_AGGREGATION_MOC|P03 Period Aggregation and Completeness v2]]

## وضعیت

- P00 package کامل است ولی ADRهای معمار هنوز باید نهایی شوند.
- P01، P02 و P03 کد، قرارداد، تست، داکیومنت و Obsidian دارند؛ compile واقعی MetaEditor برای هر Expert لازم است.
- Weekly و WW تا ADR-DY-A03 غیرفعال‌اند.
- P04 Declarative 22-Relationship Registry: implemented.
- P05 Touch-Only Hunt Observation: implemented; awaiting MetaEditor/runtime evidence.
- مرحله بعدی رسمی: P06 Host-Timeframe Close Confirmation State Machine.
- هیچ فاز فعلی execution authority ندارد.

- [[12_phase05_hunt_observation_v2/00_INDEX|Phase 05 — Touch-Only Hunt Observation v2]]
