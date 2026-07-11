---
title: "Multi-Symbol Synchronization"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Objective

A multi-symbol anatomy must not compare bars merely because both arrays have a “latest” element. The elements must satisfy explicit temporal readiness.

## Requirement contract

Each required series declares:

- symbol;
- timeframe;
- maximum close-time skew;
- maximum staleness.

## Evaluation

The synchronizer checks:

1. every series exists;
2. no series is gapped;
3. every latest close is sufficiently fresh;
4. maximum close minus minimum close is within tolerance.

The result includes status, minimum and maximum close times, skew, counts, and detail.

## Fail-closed statuses

- missing series;
- gapped series;
- stale series;
- skew exceeded.

No downstream event may be emitted from a synchronization failure in live-capable modes.

## Event clustering consequence

Synchronization establishes what was concurrently knowable. It does not imply statistical independence. Event-cluster identity and anti-overfit splitting remain separate later responsibilities.

## Future refinement

Some strategies may require as-of joins rather than equal closes. Phase 03 deliberately provides tolerances instead of hardcoding equality. A future synchronization policy plugin may implement as-of behavior while preserving the same readiness result contract.
