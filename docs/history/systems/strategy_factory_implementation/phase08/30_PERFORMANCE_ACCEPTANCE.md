---
title: "Performance Acceptance"
phase: 08
status: canonical
---
# Performance Acceptance

Phase 08 measures candidate-build latency independently from anatomy and context latency. Initial acceptance requires bounded work proportional only to the compiled template count, no allocation explosion and stable P99 under the configured matrix size. Hardware-specific thresholds are recorded during local benchmarks.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
