---
id: EXP0018-P01-08-TRANSITION-EVENT-MODEL
title: "EXP0018 P01 — Transition Event Model"
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


# Eventها

- `KERNEL_INITIALIZED`
- `DST_OFFSET_CHANGED`
- `TRADING_DAY_OPENED`
- `SESSION_CHANGED`
- `SUBCYCLE_CHANGED`
- `GAP_ENTERED`
- `GAP_EXITED`

Event ID deterministic است:

```text
EXP0018|P01|<TYPE>|<EVENT_TIME_UTC>|<TO_PERIOD>
```

اگر timer چند ثانیه دیر callback بدهد، `event_time_utc` boundary واقعی است و `availability_time_utc` لحظه مشاهده. retry با همان identity event جدید منطقی تولید نمی‌کند.

