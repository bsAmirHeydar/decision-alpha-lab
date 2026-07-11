---
title: "Strategy Factory Phase 04 — Static Plugin Registry and Anatomy Adapter SDK"
status: implemented-pending-local-compile
tags: [strategy-factory, mql5, plugins, anatomy, phase04]
---

# Phase 04 — Static Plugin Registry and Anatomy Adapter SDK

> Central engine only. No legacy strategy integration is performed in this phase.

## Canonical flow

```text
Shared Market Services
→ Exact Static Plugin Selection
→ Requirement Validation
→ Anatomy Plugin Lifecycle
→ Bounded Canonical Event Queue
→ Runtime Event-to-Snapshot Path
```

## Documents

- [[01_PHASE_CHARTER_AND_EXIT_GATE|Phase Charter and Exit Gate]]
- [[02_REFERENCE_ARCHITECTURE|Reference Architecture]]
- [[03_STATIC_REGISTRY_DECISION|Static Registry Decision]]
- [[04_PLUGIN_DESCRIPTOR_CONTRACT|Plugin Descriptor Contract]]
- [[05_CAPABILITY_MODEL|Capability Model]]
- [[06_UPDATE_SCOPE_MODEL|Update Scope Model]]
- [[07_RESOURCE_REQUIREMENTS|Market Resource Requirements]]
- [[08_ANATOMY_ADAPTER_SDK|Anatomy Adapter SDK]]
- [[09_PLUGIN_LIFECYCLE|Plugin Lifecycle]]
- [[10_BOUNDED_EVENT_QUEUE|Bounded Anatomy Event Queue]]
- [[11_IDEMPOTENCY_AND_CLUSTERING|Idempotency and Event Clustering]]
- [[12_STARTUP_READINESS_VALIDATION|Startup Readiness Validation]]
- [[13_SHARED_SERVICE_BINDING|Shared Service Binding]]
- [[14_FACTORY_AND_EXACT_VERSION|Factory and Exact Version Selection]]
- [[15_CONFIGURATION_HASHING|Configuration Hashing]]
- [[16_FAST_PATH_AND_AUDIT_PATH|Fast Path and Audit Path]]
- [[17_FAIL_CLOSED_SEMANTICS|Fail-Closed Semantics]]
- [[18_PLUGIN_TELEMETRY|Plugin Telemetry and Health]]
- [[19_FIXTURE_PLUGIN|Fixture Pulse Anatomy]]
- [[20_CENTRAL_HOST_COMPOSITION|Central Host Composition]]
- [[21_PYTHON_CONFORMANCE_MIRROR|Python Conformance Mirror]]
- [[22_PLUGIN_MANIFEST_SCHEMA|Plugin Manifest Schema]]
- [[23_GOLDEN_FIXTURE_PROTOCOL|Golden Fixture Protocol]]
- [[24_REPLAY_DETERMINISM|Replay Determinism]]
- [[25_PLUGIN_ADMISSION_GATE|Plugin Admission Gate]]
- [[26_SECURITY_AND_AUTHORITY|Security and Authority Boundary]]
- [[27_PERFORMANCE_AND_LATENCY|Performance and Latency Budget]]
- [[28_MEMORY_AND_QUEUE_POLICY|Memory and Queue Policy]]
- [[29_TEST_MATRIX|Phase 04 Test Matrix]]
- [[30_COMPILE_AND_RUNBOOK|Compile and Local Runbook]]
- [[31_NEW_ANATOMY_WORK_PACKET|New Anatomy Work Packet]]
- [[32_SCAFFOLDING_TOOL|Scaffolding Tool]]
- [[33_DEPENDENCY_BOUNDARIES|Dependency Boundaries]]
- [[34_PHASE05_HANDOFF|Phase 05 Handoff]]
- [[35_DEFINITION_OF_DONE|Definition of Done]]
- [[36_LIMITATIONS_AND_DEFERRED|Limitations and Deferred Decisions]]
- [[37_REGISTRY_API_REFERENCE|Registry API Reference]]
- [[38_PLUGIN_BASE_API_REFERENCE|Plugin Base API Reference]]
- [[39_STARTUP_VALIDATOR_API|Startup Validator API Reference]]
- [[40_QUEUE_API_REFERENCE|Event Queue API Reference]]
- [[41_RUNTIME_INTEGRATION_SEQUENCE|Runtime Integration Sequence]]
- [[42_VERSIONING_AND_MIGRATION|Versioning and Migration]]
- [[43_MULTI_SYMBOL_AND_MTF|Multi-Symbol and Multi-Timeframe Declaration]]
- [[44_OBSERVABILITY_CATALOG|Observability Catalog]]
- [[45_DECISION_LOG|Architecture Decision Log]]

## Machine-readable evidence

- `lab/11_strategy_factory/phase04_plugins/artifacts/`
- `lab/11_strategy_factory/implementation_program/phase_status/PHASE_04.json`
- `lab/11_strategy_factory/implementation_program/phase_status/PHASE_04_HANDOFF_TO_PHASE_05.json`
