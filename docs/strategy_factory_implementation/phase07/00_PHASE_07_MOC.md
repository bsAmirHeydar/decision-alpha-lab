---
title: "Phase 07 — Context State, Feature DAG, and Immutable Feature Frames"
phase: 07
status: implemented-pending-local-mql5-compile
---
# Phase 07 MOC

Phase 07 turns a canonical MQL5 anatomy event into a causally valid, dependency-ordered, immutable feature snapshot and a fixed-order numeric vector. The central engine remains strategy-neutral.

## Core flow

```text
AnatomyEvent
→ Context generation
→ Dirty invalidation
→ Topological feature computation
→ Feature quality and known-time validation
→ Immutable FeatureSnapshot
→ Fixed FeatureVector
→ ContextFrame identity
```

## Navigation

- [[01_PHASE_CHARTER]]
- [[02_CONTEXT_AUTHORITY_MODEL]]
- [[03_FEATURE_DESCRIPTOR_CONTRACT]]
- [[04_FEATURE_PROVIDER_REGISTRY]]
- [[05_DEPENDENCY_DAG_COMPILER]]
- [[06_DIRTY_GENERATION_PROPAGATION]]
- [[07_CONTEXT_STATE_STORE]]
- [[08_FEATURE_FRESHNESS_AND_TTL]]
- [[09_IMMUTABLE_FEATURE_SNAPSHOT]]
- [[10_CONTEXT_FRAME_IDENTITY]]
- [[11_FIXED_FEATURE_VECTOR_SCHEMA]]
- [[12_MISSING_QUALITY_AND_FAIL_CLOSED]]
- [[13_CAUSAL_TIME_ENFORCEMENT]]
- [[14_INCREMENTAL_RECOMPUTATION_MODEL]]
- [[15_PERFORMANCE_AND_MEMORY_BOUNDS]]
- [[16_TELEMETRY_AND_HEALTH]]
- [[17_REFERENCE_FEATURE_PACK]]
- [[18_HOST_COMPOSITION]]
- [[19_MQL5_API_REFERENCE]]
- [[20_PYTHON_CONFORMANCE_BOUNDARY]]
- [[21_SCHEMA_REGISTRY]]
- [[22_TEST_MATRIX]]
- [[23_GOLDEN_CONTEXT_FIXTURES]]
- [[24_FAILURE_SEMANTICS]]
- [[25_SECURITY_AND_CAPITAL_BOUNDARY]]
- [[26_DEFINITION_OF_DONE]]
- [[27_PHASE08_HANDOFF]]
- [[PHASE_07_ARCHITECTURE.canvas]]
