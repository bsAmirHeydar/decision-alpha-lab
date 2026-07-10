---
id: EXP0018-P01-12-TEST-FIXTURE-PLAN
title: "EXP0018 P01 — Test Fixture Plan"
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


# Test layers

## Embedded MQL5

- spring forward قبل/بعد؛
- fall back قبل/بعد و fold؛
- 17:59:59 و 18:00؛
- p3/p4 boundary؛
- trading-day key rollover.

## Python Reference

- golden UTC→NY fixtureها؛
- exhaustive 86400-second classification؛
- repeated 01:30 fall-back؛
- p4 30-minute contract؛
- weekly disabled؛
- execution authority false.

## MetaEditor/Runtime

- 0 errors / 0 warnings؛
- attach/detach؛
- timer restart؛
- CSV open failure؛
- manual and auto offset diagnostics.

