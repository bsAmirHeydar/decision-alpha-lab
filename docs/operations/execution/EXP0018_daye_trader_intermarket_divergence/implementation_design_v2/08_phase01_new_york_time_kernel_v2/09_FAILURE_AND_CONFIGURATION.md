---
id: EXP0018-P01-09-FAILURE-AND-CONFIGURATION
title: "EXP0018 P01 — Failure and Configuration"
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


# وضعیت‌های صریح

```text
OK
INVALID_INPUT
INVALID_CONFIG
UNAVAILABLE
AMBIGUOUS_LOCAL_TIME
NONEXISTENT_LOCAL_TIME
IO_ERROR
```

هیچ failure به `NONE session` تبدیل نمی‌شود. `NONE` فقط وضعیت معتبر gap است.

## Configuration

- broker offset باید بین UTC-14 و UTC+14 باشد؛
- schema version باید 2 باشد؛
- auto broker offset برای replay unsafe است؛
- Local ambiguity policy به‌صورت input آشکار است.

