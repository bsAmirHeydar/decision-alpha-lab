---
title: "Missing Bar and Gap Policy"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Default policy

The default is `FAIL_CLOSED`.

A missing or gapped price series cannot be converted into a valid anatomy decision by convenience. This rule protects:

- event timestamps;
- relative comparisons;
- volatility measures;
- invalidation geometry;
- outcome ordering.

## Registered policies

### Fail closed

Permitted for all modes and mandatory for live-capable V1.

### Mark gapped

Research data-quality analysis only. It allows the artifact to preserve the observation but prohibits trading decisions.

### Forward-fill context only

Deferred. It may eventually be used for non-price contextual metadata, never for price geometry, fills, stops, or targets.

### Ignore with audit

Diagnostic only. It cannot be promoted to paper or live.

## Recovery

A gap is resolved by rebuilding the affected series from a trusted source and incrementing generation. The recovery operation must emit an audit record. Clearing a Boolean flag without rebuilding is prohibited.

## Strategy boundary

An anatomy plugin may declare that a series is optional. It may not redefine a required gapped series as valid after runtime initialization.
