---
title: "Failure Semantics and Fail-Closed Rules"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Failure classes

## Configuration failure

Examples: invalid broker offset, invalid capacity, unsafe symbol. Result: initialization fails.

## Source failure

Examples: `CopyRates` returns no data, `SymbolInfoTick` fails. Result: source-error telemetry and no new valid state.

## Contract failure

Examples: invalid OHLC geometry, future bar close, out-of-order tick. Result: record rejected.

## Quality failure

Examples: stale tick, gapped series, synchronization skew. Result: consumer receives failure and must abstain.

## Drift failure

Example: symbol specification changes while active geometry exists. Result: generation changes; later execution layers must revalidate.

## Recovery

Recovery must be explicit and observable. Retrying a source is acceptable; silently converting invalid data to defaults is not.

# Fail-closed invariant

No required market-state failure may be transformed into a trade approval by a downstream plugin. Risk and execution layers may only further restrict authority.
