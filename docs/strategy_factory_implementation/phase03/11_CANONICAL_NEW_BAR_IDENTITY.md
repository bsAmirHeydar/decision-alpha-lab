---
title: "Canonical New-Bar Identity"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Problem

Many EAs infer a new bar by comparing local timestamps, counters, or chart state. In multi-symbol systems this produces duplicate or missed callbacks.

## Solution

`CSF03NewBarTracker` observes validated `SF01_BarRecord` values keyed by symbol and timeframe. It records:

- last open UTC milliseconds;
- last canonical bar ID.

## Outcomes

- first valid observation: new bar;
- identical canonical ID: not new;
- same open time with replacement content: update identity, not new;
- later open time: new bar;
- historical regression: reject.

## Design consequence

An anatomy plugin will not maintain its own `last_bar_time`. It subscribes to a future plugin callback driven by this tracker or queries generation changes.

## Replay parity

Because new-bar identity is based on canonical bar records, tester, paper, and replay modes can reproduce the same transition behavior.
