---
title: "Performance and Latency Budgets"
---

# Performance and Latency Budgets

Phase 02 does not yet contain the final decision path, but it establishes bounded behavior.

## Bounded Work

- Event draining is capped per callback.
- Audit queue capacity is fixed.
- No file parsing occurs in `OnTick`.
- No dynamic plugin discovery occurs in `OnTick`.
- No full-history scan exists in the Host.
- No statistical or model-training code exists in the runtime.

## Preliminary Budgets

| Segment | Initial engineering target |
|---|---:|
| Host callback overhead | under 0.10 ms median |
| Event validation | under 0.05 ms per event |
| Empty/null path | under 0.05 ms median |
| Event-to-snapshot fixture path | under 1 ms P99 in reference tests |
| Audit publish | under 0.05 ms per record |

These are design targets, not production guarantees. Phase 19 will own formal telemetry and SLO enforcement.

## Allocation Policy

Arrays are sized during initialization where possible. The audit ring does not grow after startup. Later candidate and feature-vector paths must use precompiled fixed schemas and bounded candidate counts.

## Slow-Path Separation

Serialization, file flush, report generation and model training belong outside the hot path. The Result Sink interface allows a buffered implementation later while keeping runtime semantics unchanged.
