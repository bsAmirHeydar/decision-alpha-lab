---
id: EXP0018-P03-MQL5
title: "P03 MQL5 Module Architecture"
type: spec
status: active
project: EXP0018
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - phase03
  - period-aggregation
---

# معماری ماژول‌های MQL5

- `DAYE_PeriodTypes`: schema و enum
- `DAYE_PeriodIdentity`: identity و UTC→NY snapshot
- `DAYE_PeriodAggregator`: pure aggregation و completeness
- `DAYE_PeriodStore`: query و summary
- `DAYE_PeriodEvents`: event detection
- `DAYE_PeriodDiagnostics`: logging
- `DAYE_PeriodAudit`: CSV adapter
- `DAYE_PeriodSelfTest`: embedded tests
- `DAYE_PeriodEngine`: runtime state owner
- `EXP0018_Daye_Period_Anatomy`: inputs و timer

Detection، I/O و mutable state در یک فایل مخلوط نشده‌اند.
