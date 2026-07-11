---
title: "Phase 08 — Candidate Policy Engine MOC"
phase: 08
status: canonical
---
# Phase 08 — Candidate Policy Registry and Deterministic Candidate Matrix

## Core flow

```text
AnatomyEvent + FeatureSnapshot + ContextFrame
→ exact policy registry
→ compiled candidate matrix
→ admissibility
→ entry/stop/exit geometry
→ central validation
→ stable TradeCandidate IDs
→ bounded candidate queue
```

## Documents

- [[01_PHASE_CHARTER|Phase Charter]]
- [[02_AUTHORITY_AND_BOUNDARIES|Authority and Boundaries]]
- [[03_CANDIDATE_DOMAIN_MODEL|Candidate Domain Model]]
- [[04_POLICY_PLUGIN_CONTRACTS|Policy Plugin Contracts]]
- [[05_POLICY_REGISTRY|Policy Registry]]
- [[06_POLICY_PARAMETERS|Policy Parameters]]
- [[07_CANDIDATE_TEMPLATE|Candidate Template]]
- [[08_MATRIX_COMPILATION|Matrix Compilation]]
- [[09_ADMISSIBILITY_PROTOCOL|Admissibility Protocol]]
- [[10_ENTRY_POLICY_ARCHITECTURE|Entry Policy Architecture]]
- [[11_STOP_POLICY_ARCHITECTURE|Stop Policy Architecture]]
- [[12_EXIT_POLICY_ARCHITECTURE|Exit Policy Architecture]]
- [[13_TRADE_CANDIDATE_IDENTITY|Trade Candidate Identity]]
- [[14_DIRECTIONAL_GEOMETRY|Directional Geometry]]
- [[15_BOUNDED_ENUMERATION|Bounded Enumeration]]
- [[16_DETERMINISTIC_ORDERING|Deterministic Ordering]]
- [[17_DUPLICATE_PREVENTION|Duplicate Prevention]]
- [[18_CONTEXT_IMMUTABILITY|Context Immutability]]
- [[19_FAST_PATH_POLICY|Fast Path Policy]]
- [[20_TELEMETRY_AND_HEALTH|Telemetry and Health]]
- [[21_REFERENCE_POLICY_PACK|Reference Policy Pack]]
- [[22_RESEARCH_MATRIX_VS_RUNTIME_MATRIX|Research Matrix vs Runtime Matrix]]
- [[23_TRIAL_IDENTITY_AND_MULTIPLE_TESTING|Trial Identity and Multiple Testing]]
- [[24_FAILURE_SEMANTICS|Failure Semantics]]
- [[25_SECURITY_AND_CAPITAL_BOUNDARY|Security and Capital Boundary]]
- [[26_PYTHON_CONFORMANCE_BOUNDARY|Python Conformance Boundary]]
- [[27_SCHEMA_AND_ARTIFACTS|Schema and Artifacts]]
- [[28_TEST_MATRIX|Test Matrix]]
- [[29_GOLDEN_CANDIDATE_FIXTURES|Golden Candidate Fixtures]]
- [[30_PERFORMANCE_ACCEPTANCE|Performance Acceptance]]
- [[31_MQL5_API_REFERENCE|MQL5 API Reference]]
- [[32_PYTHON_API_REFERENCE|Python API Reference]]
- [[33_DEFINITION_OF_DONE|Definition of Done]]
- [[34_PHASE09_HANDOFF|Phase 09 Handoff]]
- [[35_IMPLEMENTATION_RUNBOOK|Implementation Runbook]]
