---
title: Strategy Factory Phase 01 — MQL5-First Contracts and Schema
tags: [strategy-factory, phase-01, mql5-first, contracts, schema]
status: implemented
---

# Phase 01 — MQL5-First Contracts and Schema

This phase freezes the language spoken by every later Strategy Factory module. MQL5 is the primary runtime authority. Python is a research mirror, validator, trainer input layer, and compatibility consumer. Neither side is allowed to invent a second interpretation of the same event.

## Navigation

- [[01_PHASE_CHARTER_AND_AUTHORITY_MODEL]]
- [[02_MQL5_FIRST_ARCHITECTURE]]
- [[03_CANONICAL_CONTRACT_CATALOG]]
- [[04_TIME_AND_CAUSALITY_CONTRACT]]
- [[05_IDENTITY_HASHING_AND_IDEMPOTENCY]]
- [[06_SCHEMA_VERSIONING_AND_COMPATIBILITY]]
- [[07_BAR_RECORD_CONTRACT]]
- [[08_ANATOMY_EVENT_CONTRACT]]
- [[09_FEATURE_VALUE_AND_SNAPSHOT_CONTRACT]]
- [[10_ARTIFACT_IDENTITY_AND_LINEAGE]]
- [[11_SERIALIZATION_AND_WIRE_FORMATS]]
- [[12_PYTHON_MIRROR_BOUNDARY]]
- [[13_CROSS_LANGUAGE_CONFORMANCE]]
- [[14_VALIDATION_AND_FAILURE_SEMANTICS]]
- [[15_PERFORMANCE_AND_ALLOCATION_POLICY]]
- [[16_SECURITY_AND_CAPITAL_AUTHORITY_BOUNDARY]]
- [[17_TEST_MATRIX_AND_ACCEPTANCE_GATE]]
- [[18_MIGRATION_GUIDE_FOR_EXISTING_ANATOMIES]]
- [[19_PHASE_02_HANDOFF]]
- [[20_FIELD_LEVEL_SCHEMA_REFERENCE]]
- [[21_MQL5_API_REFERENCE]]
- [[22_PYTHON_API_REFERENCE]]
- [[23_COMPILE_AND_TEST_RUNBOOK]]
- [[24_DEFINITION_OF_DONE_AND_EVIDENCE]]
- [[25_KNOWN_LIMITATIONS_AND_DEFERRED_DECISIONS]]
- [[adrs/ADR_0101_MQL5_IS_RUNTIME_CONTRACT_AUTHORITY]]
- [[adrs/ADR_0102_PYTHON_IS_A_STRICT_MIRROR_NOT_A_SECOND_CANON]]
- [[adrs/ADR_0103_STABLE_IDS_USE_FNV1A64_UTF16LE]]
- [[adrs/ADR_0104_UTC_EPOCH_MILLISECONDS_IS_CANONICAL_TIME]]
- [[adrs/ADR_0105_CONTRACTS_FAIL_CLOSED]]

## Implemented deliverables

1. MQL5 contract kernel under `mql5/Include/AlphaLab/StrategyFactory/Contracts`.
2. MQL5 self-test EA under `mql5/Experts/StrategyFactoryTests`.
3. Python mirror package under `lab/11_strategy_factory/python/strategy_factory_contracts`.
4. Machine-readable schema registry and JSON Schemas.
5. Cross-language golden vectors.
6. Automated Python tests and MQL5 static conformance tests.
7. PowerShell MetaEditor compilation harness.
8. Phase status, QA evidence, file hashes, and Phase 02 handoff.

## Non-goals

This phase does not implement feature DAGs, candidate generation, outcome simulation, model training, paper trading, portfolio risk, or live order submission. It defines the contracts those later systems must obey.
