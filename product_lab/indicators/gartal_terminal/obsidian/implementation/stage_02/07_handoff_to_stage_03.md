---
title: Stage 02 — Handoff to Stage 03
type: handoff
stage: 02
---

# Handoff to Stage 03

Stage 03 can now focus exclusively on broker GMT and time normalization.

## What Stage 03 receives

- `time_source`, `time_utc`, and `time_broker` fields already exist.
- `GT_SourceToBrokerTime`, `GT_UtcToBrokerTime`, and `GT_BrokerToUtcTime` exist.
- sample events are currently added in broker time for predictable chart testing.
- date-window functions already operate on broker time.

## What Stage 03 must add

- stricter auto GMT detection audit;
- manual override diagnostics;
- source GMT interpretation contract;
- UTC-first sample mode option;
- DST notes and broker-session verification;
- visible debug labels for detected broker offset.

## Must not do in Stage 03

- do not implement Forex Factory parsing;
- do not redesign dashboard interactions;
- do not build the final luxury UI;
- do not create the alert state machine beyond existing hooks.
