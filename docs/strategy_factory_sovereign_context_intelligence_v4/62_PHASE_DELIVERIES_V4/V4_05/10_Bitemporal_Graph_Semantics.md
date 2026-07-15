---
title: Bitemporal Graph Semantics
status: implemented
version: 1.0.0
phase: V4-05
created: '2026-07-15'
updated: '2026-07-15'
capability_tier: core-production-context-plane
tags: [saed-v4, v4-05, semantic-temporal-hypergraph]
---

# Bitemporal Graph Semantics

## Purpose

Every node and edge is constrained by both event time and known time. Event time states when the represented evidence occurred; known time states when it became available to the system. Both must lie within the graph boundaries, and known time cannot precede event time. Edge intervals are derived from member nodes and may not be inverted.

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

- Previous: [[09_Allowlisted_Semantic_Rules]]
- Phase home: [[00_MOC_V4_05_Semantic_And_Temporal_Hypergraph]]
- Next: [[11_Known_Time_And_Event_Time_Gates]]
