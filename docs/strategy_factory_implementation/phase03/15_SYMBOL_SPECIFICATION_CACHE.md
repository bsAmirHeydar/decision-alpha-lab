---
title: "Symbol Specification Cache"
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

Broker metadata is not static. It must be treated as versioned runtime state.

## Snapshot fields

- digits;
- point;
- tick size;
- tick value;
- contract size;
- minimum, maximum, and step volume;
- stops and freeze levels;
- filling, order, and trade modes;
- observed time;
- quality;
- specification generation.

## Material equality

Observation time does not trigger a generation change. A generation changes only when a material execution field changes.

## Consumers

Later modules will use the cache for:

- price normalization;
- risk-distance conversion;
- volume sizing;
- stop-level validation;
- request construction;
- broker capability gates.

## Failure

A specification with non-positive point, tick size, or volume step is invalid. The runtime must not guess defaults.

## Source ownership

Only `CSF03TerminalMarketSource` reads terminal symbol properties. Strategies consume the cache through `ISF02SymbolSpecPort`.
