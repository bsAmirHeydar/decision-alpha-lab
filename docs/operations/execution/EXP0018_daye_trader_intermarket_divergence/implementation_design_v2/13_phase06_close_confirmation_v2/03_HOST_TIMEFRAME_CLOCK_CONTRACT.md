---
id: EXP0018-P06-HOST-CLOCK
title: "P06 Host Timeframe Clock Contract"
type: implementation-note
status: implemented
project: EXP0018
phase: P06
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - p06
  - confirmation
---

# Host timeframe clock

`PERIOD_CURRENT` resolves to the timeframe of the chart carrying the Expert. An explicit timeframe can be selected for controlled research.

## Gates

- host timeframe must have fixed seconds;
- host timeframe must be an integer multiple of the base timeframe;
- symbol A and B host bars must have the same UTC open timestamp;
- current and latest closed host bars must be independently readable;
- closed bar identity is based on timeframe, UTC open, and canonical symbol pair.

Index equality is forbidden. Approximate timestamp matching is forbidden.
