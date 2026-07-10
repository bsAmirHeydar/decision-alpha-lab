---
id: EXP0018-P01-10-MQL5-MODULE-ARCHITECTURE
title: "EXP0018 P01 — MQL5 Module Architecture"
type: specification
status: implemented-awaiting-metaeditor-compile
project: EXP0018
phase: P01
version: 2.2.0
created: 2026-07-10
updated: 2026-07-10
owner: Quant Engineering
tags:
  - exp0018
  - daye-trader
  - phase01
  - time-kernel
---


# ماژول‌ها

| Module | Ownership |
|---|---|
| `DAYE_Types` | enum و contract types |
| `DAYE_Time` | تبدیل pure و DST |
| `DAYE_PeriodRegistry` | definitionهای declarative |
| `DAYE_Calendar` | classification و window construction |
| `DAYE_TimeEvents` | transition detection |
| `DAYE_TimeAudit` | CSV adapter اختیاری |
| `DAYE_Diagnostics` | formatting/printing |
| `DAYE_TimeSelfTest` | self-test embedded |
| `DAYE_Engine` | state owner و orchestration |
| Expert | inputs، timer و lifecycle |

Pure calculation از I/O جدا شده است. State قبلی فقط در Engine mutable است.

