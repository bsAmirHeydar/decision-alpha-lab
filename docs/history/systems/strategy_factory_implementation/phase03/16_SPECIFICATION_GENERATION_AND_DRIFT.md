---
title: "Specification Generation and Drift"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Generation model

The first accepted specification receives generation 1. A materially identical refresh preserves generation. A material difference increments generation.

## Why generations matter

A decision generated under one tick size or volume step may not remain executable after a specification change. Context, candidate, and execution artifacts must eventually carry the specification generation they used.

## Drift examples

- broker changes minimum lot;
- CFD contract size changes;
- symbol switches trade mode;
- stops level widens;
- filling mode changes;
- tick value changes after contract rollover.

## Operational response

Material drift should:

1. emit telemetry and audit;
2. invalidate affected cached execution geometry;
3. force risk and broker validation to refresh;
4. block live intents until consistency is restored.

Phase 03 implements detection and generation. Full incident response is owned by later risk/execution phases.
