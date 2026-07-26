---
title: Strategy Factory Phase 06 — Reference Anatomy Adapter and Golden Event Ledger
status: implemented-pending-local-mql5-compile
phase: 06
tags: [strategy-factory, mql5, anatomy, golden-ledger, adapter-sdk]
---
# Phase 06 MOC

Phase 06 proves the central engine can consume a real, deterministic, closed-bar anatomy plugin without importing any legacy strategy.

## Core flow

```text
Shared Market Services
→ Static Plugin Registry
→ Immutable Runtime Generation
→ Reference Anatomy Observation
→ Canonical Anatomy Event
→ Feature Snapshot
→ Versioned Result Sink
→ Golden Event Ledger
```

## Navigation

- [[01_PHASE_CHARTER]]
- [[02_CENTRAL_ENGINE_ONLY_POLICY]]
- [[03_ANATOMY_ADAPTER_SDK]]
- [[04_OBSERVATION_CONTRACT]]
- [[05_EVENT_LIFECYCLE]]
- [[06_REFERENCE_ANATOMY_ALGORITHM]]
- [[07_GOLDEN_LEDGER_PROTOCOL]]
- [[08_EVENT_IDENTITY_AND_CLUSTERING]]
- [[09_KNOWN_TIME_AND_CLOSED_BAR_POLICY]]
- [[10_HOST_COMPOSITION]]
- [[11_RESULT_SINK_INTEGRATION]]
- [[12_REPLAY_AND_DIFFERENTIAL_TESTING]]
- [[13_MQL5_API_REFERENCE]]
- [[14_PYTHON_CONFORMANCE_BOUNDARY]]
- [[15_TEST_MATRIX]]
- [[16_PERFORMANCE_BUDGET]]
- [[17_FAILURE_SEMANTICS]]
- [[18_SECURITY_AND_CAPITAL_BOUNDARY]]
- [[19_DEFINITION_OF_DONE]]
- [[20_PHASE07_HANDOFF]]
