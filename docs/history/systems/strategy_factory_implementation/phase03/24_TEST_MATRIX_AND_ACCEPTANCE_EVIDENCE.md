---
title: "Test Matrix and Acceptance Evidence"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Automated tests

## Time

- winter/summer New York offsets;
- exact DST boundaries;
- broker-to-UTC conversion;
- naive datetime rejection;
- trading-day rollover.

## Sessions

- DST session resolution;
- cross-midnight intervals;
- duplicate ID rejection.

## Caches

- out-of-order ticks;
- stale ticks;
- insert/replace/duplicate bars;
- persistent gaps;
- bounded capacity.

## Synchronization

- ready;
- missing;
- skew exceeded;
- gap detected.

## Specifications

- initial generation;
- no generation on equivalent refresh;
- generation increment on material drift.

## Compatibility hotfix

- broker prefixes/suffixes accepted;
- wire delimiters, spaces, and controls rejected.

## Static architecture

- expected MQL5 modules exist;
- terminal APIs are isolated;
- no order authority exists.

# Local MQL5 tests

`SF03_MarketServicesSelfTest.mq5` repeats core behavior inside MetaEditor/terminal semantics.

# Acceptance evidence

Automated tests are necessary but not sufficient. The phase remains pending local acceptance until MetaEditor compilation and broker diagnostic runs are attached to the phase status.
