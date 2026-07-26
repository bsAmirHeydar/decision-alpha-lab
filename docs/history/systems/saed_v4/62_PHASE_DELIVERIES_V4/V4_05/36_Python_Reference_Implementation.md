---
title: Python Reference Implementation
status: implemented
version: 1.0.0
phase: V4-05
created: '2026-07-15'
updated: '2026-07-15'
capability_tier: core-production-context-plane
tags: [saed-v4, v4-05, semantic-temporal-hypergraph]
---

# Python Reference Implementation

## Purpose

The Python package is saed_v4_semantic_hypergraph. It uses immutable dataclasses, canonical JSON hashing, explicit enums, closed registry and policy validation, deterministic adapters, a pure builder, integrity receipts, replay, diff, projection, bounded query, deterministic partitioning, telemetry, conformance, and a registry-inspection CLI.

## Contractual rules

1. Inputs are immutable, exact-versioned, content-addressed, point-in-time correct, and bound to one Evidence Role.
2. Unknown, stale, unsupported, hash-mismatched, cross-role, over-budget, or authority-violating states fail closed.
3. Operational ordering, request IDs, cache locations, process IDs, and runtime scheduling are not semantic inputs.
4. Every accepted output is reconstructible from the source package hash, registry hash, policy hash, temporal boundaries, and code version.
5. UCEE remains authority of record; this phase grants no training, Treatment selection, portfolio, runtime, broker, or order authority.

## Implementation evidence

The reference implementation is located in `lab/11_strategy_factory/python/saed_v4_semantic_hypergraph`. Closed contracts are in `lab/11_strategy_factory/schemas/saed_v4_05`; examples and negative fixtures are in `lab/11_strategy_factory/examples/saed_v4_05`; tests are in `lab/11_strategy_factory/tests/phase_saed_v4_05_semantic_temporal_hypergraph`; and the diagnostic-only MQL5 mirror is in `mql5/Include/AlphaLab/StrategyFactory/SAEDV4SemanticHypergraph`.

## Failure posture

There is no silent repair. Invalid source identity, future visibility, cross-role evidence, unknown relation type, invalid arity, dangling incidence, duplicate identity, hash mismatch, exceeded capacity, or forbidden authority produces rejection or quarantine. External evidence that is unavailable remains explicitly pending.

## Navigation

- Previous: [[35_Service_API]]
- Phase home: [[00_MOC_V4_05_Semantic_And_Temporal_Hypergraph]]
- Next: [[37_MQL5_Diagnostic_Mirror]]
