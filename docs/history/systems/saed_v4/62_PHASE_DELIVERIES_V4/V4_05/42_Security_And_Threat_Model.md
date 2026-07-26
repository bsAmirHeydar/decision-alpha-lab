---
title: Security And Threat Model
status: implemented
version: 1.0.0
phase: V4-05
created: '2026-07-15'
updated: '2026-07-15'
capability_tier: core-production-context-plane
tags: [saed-v4, v4-05, semantic-temporal-hypergraph]
---

# Security And Threat Model

## Purpose

Primary threats are contract smuggling, future leakage, outcome leakage, registry tampering, dense-graph denial of service, identity collision through unstable inputs, cross-role contamination, descriptor authority escalation, stale cache substitution, and false claims from static MQL5 checks. Controls are closed schemas, hash binding, budgets, explicit authority, replay, and evidence classification.

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

- Previous: [[41_Mutation_And_Adversarial_Tests]]
- Phase home: [[00_MOC_V4_05_Semantic_And_Temporal_Hypergraph]]
- Next: [[43_Incident_Quarantine_And_Recovery]]
