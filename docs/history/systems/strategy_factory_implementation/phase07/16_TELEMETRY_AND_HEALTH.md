---
title: "Telemetry and Health"
phase: 07
status: canonical
---
# Telemetry and Health

Counters cover builds, failures, computations, cache hits, stale and missing rejections, dependency failures, vector builds, total latency and maximum latency. Health becomes degraded or failed explicitly.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
