---
title: "Tick Cache Reference"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Purpose

The tick cache keeps one validated latest snapshot per symbol. It prevents repeated terminal calls and provides explicit receive-time freshness.

## Stored fields

- terminal symbol;
- original `MqlTick`;
- receive time in UTC milliseconds;
- source generation;
- quality state.

## Validation

The cache rejects:

- unsafe terminal symbols;
- negative times;
- non-finite prices;
- ask below bid;
- source-time regression.

Retrieval rejects:

- unknown symbols;
- receive times in the future;
- ticks older than the configured maximum age.

## Why receive time matters

Source time and local receive time answer different questions. Source time describes the broker event; receive time measures how stale the locally available state is. Later latency telemetry can compare them without changing the tick contract.

## Scope

The Phase 03 cache is a latest-tick cache, not a tick-history database. Detailed tick replay and outcome simulation will use separate bounded streams and artifacts in later phases.
