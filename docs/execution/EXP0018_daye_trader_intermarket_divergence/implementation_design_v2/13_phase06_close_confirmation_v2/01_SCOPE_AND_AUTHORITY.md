---
id: EXP0018-P06-SCOPE
title: "P06 Scope and Authority"
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

# Scope

P06 owns only the transition from **live one-sided P05 fact** to **first-host-close outcome**.

## Authoritative inputs

- P05 observation identity and pair state;
- source availability timestamp;
- exact closed host bars for both symbols;
- host timeframe selected by the chart or explicit input.

## Owned truth

- candidate opened by a live state transition;
- target host bar identity;
- pair state as of the target close;
- final typed outcome;
- host-bar endpoint geometry for the Hunter symbol.

## Explicitly outside P06

- BUY/SELL mapping;
- First Sweep and reference retirement;
- chart object creation;
- session boxes, TWO, or TDO;
- risk, targets, orders, or model authority;
- retroactive history reconstruction without chronological replay.
