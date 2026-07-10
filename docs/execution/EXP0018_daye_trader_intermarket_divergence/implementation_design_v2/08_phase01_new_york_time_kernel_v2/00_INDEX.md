---
id: EXP0018-P01-00-INDEX
title: "EXP0018 P01 — New York Time Kernel v2 Index"
type: index
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


# P01 — هسته زمان نیویورک و تقویم

این فاز اولین لایه اجرایی Core است. خروجی آن «ساعت دامنه‌ای» است، نه سیگنال.

## مسیر مطالعه

1. [[01_SCOPE_AND_BOUNDARY]]
2. [[02_DOMAIN_TIME_MODEL]]
3. [[03_BROKER_TO_UTC_ADAPTER]]
4. [[04_NEW_YORK_DST_ALGORITHM]]
5. [[05_TRADING_DAY_AND_GAP]]
6. [[06_SESSION_AND_SUBCYCLE_WINDOWS]]
7. [[07_PERIOD_WINDOW_IDENTITY]]
8. [[08_TRANSITION_EVENT_MODEL]]
9. [[09_FAILURE_AND_CONFIGURATION]]
10. [[10_MQL5_MODULE_ARCHITECTURE]]
11. [[11_INPUT_OUTPUT_CONTRACT]]
12. [[12_TEST_FIXTURE_PLAN]]
13. [[13_RUNTIME_VALIDATION_GUIDE]]
14. [[14_PERFORMANCE_AND_DETERMINISM]]
15. [[15_SECURITY_AND_NO_EXECUTION_BOUNDARY]]
16. [[16_DEFINITION_OF_DONE]]
17. [[17_HANDOFF_TO_P02_AND_P03]]
18. [[18_ROLLBACK_PLAN]]
19. [[19_VALIDATION_REPORT]]
20. [[20_OBSIDIAN_GUIDE]]

## خروجی کد

- `DAYE_Types.mqh`
- `DAYE_Time.mqh`
- `DAYE_PeriodRegistry.mqh`
- `DAYE_Calendar.mqh`
- `DAYE_TimeEvents.mqh`
- `DAYE_TimeAudit.mqh`
- `DAYE_Diagnostics.mqh`
- `DAYE_TimeSelfTest.mqh`
- `DAYE_Engine.mqh`
- `EXP0018_Daye_Time_Foundation.mq5`

Weekly در P01 عمداً غیرفعال است تا ADR-DY-A03 پذیرفته شود.

