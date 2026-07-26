---
id: EXP0018-P01-07-PERIOD-WINDOW-IDENTITY
title: "EXP0018 P01 — Period Window Identity"
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


# هویت پنجره

هر پنجره شامل local و UTC start/end است. شناسه canonical:

```text
EXP0018|<FAMILY>|<CODE>|<START_UTC_EPOCH>
```

مثال:

```text
EXP0018|SESSION|N|1783682400
```

استفاده از UTC start باعث می‌شود دو ساعت محلی یکسان در Fall Back به‌اشتباه یک identity مبهم نسازند.

## Weekly

نوع W در registry وجود دارد اما `implementation_ready=false` است. P01 هیچ weekly window تولید نمی‌کند تا ADR-DY-A03 پذیرفته شود.

