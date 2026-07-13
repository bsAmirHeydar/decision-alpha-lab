---
title: "UCE-I02 — Context Package SDK, Lifecycle, and Reference Contexts"
tags:
  - strategy-factory
  - universal-context-engine
  - context-package-sdk
status: canonical
doc_version: 3.0.0
last_updated: 2026-07-12
---

# UCE-I02 — Context Package SDK, Lifecycle, and Reference Contexts

## Mission

UCE-I02 turns a human-defined market viewpoint into an installable, exact-versioned context package that the central engine can consume without engine modification. A package owns observation truth, feature availability, representation views, dependence clusters, manual baselines, and task declarations. It does **not** own treatment selection, money management, broker execution, or model promotion.

## Delivery Map

### Contract and package surface

- [[01_PHASE_CHARTER_AND_SCOPE]]
- [[02_CONTEXT_PACKAGE_MANIFEST_AND_INSTALLATION]]
- [[03_AUTHORITY_OWNERSHIP_AND_ENGINE_BOUNDARIES]]
- [[04_SOURCE_REQUIREMENTS_SYNCHRONIZATION_AND_AVAILABILITY]]
- [[05_CONTEXT_OBSERVATION_LIFECYCLE_STATE_MACHINE]]
- [[06_KNOWN_TIME_CAUSALITY_AND_FUTURE_PERTURBATION]]

### Feature and representation surface

- [[07_FEATURE_DESCRIPTOR_AVAILABILITY_SDK]]
- [[08_IMMUTABLE_FEATURE_FRAME_AND_ORDERING]]
- [[09_REPRESENTATION_VIEW_REGISTRY_AND_COMPILATION]]
- [[10_TABULAR_SEQUENCE_AND_MULTI_TIMEFRAME_VIEWS]]
- [[11_GRAPH_INTERMARKET_RASTER_SPARSE_PATH_AND_FUSED_VIEWS]]
- [[12_CLUSTER_AND_DEPENDENCE_RULES]]

### Human doctrine and learning declarations

- [[13_MANUAL_SETUP_AND_POLICY_ATTACHMENTS]]
- [[14_TASK_LABEL_AND_TRAINER_COMPATIBILITY_DECLARATIONS]]

### Reference packages

- [[15_SYNTHETIC_REFERENCE_CONTEXT_PACKAGE]]
- [[16_EXP0017_ADAPTER_BACKED_REFERENCE_PACKAGE]]
- [[17_REFERENCE_PACKAGE_DIFFERENTIAL_AND_PARITY_EVIDENCE]]

### Conformance and operations

- [[18_CONTEXT_PACKAGE_LINTER_AND_STATIC_CONFORMANCE]]
- [[19_REPLAY_HASH_DETERMINISM_AND_RESTART_CONFORMANCE]]
- [[20_LIFECYCLE_CHAOS_FAILURE_AND_NEGATIVE_FIXTURES]]
- [[21_PYTHON_SDK_API_REFERENCE]]
- [[22_MQL5_SDK_API_REFERENCE]]
- [[23_TEST_STRATEGY_GOLDEN_FIXTURES_AND_COVERAGE]]
- [[24_PERFORMANCE_MEMORY_AND_RESOURCE_BUDGETS]]
- [[25_SECURITY_AUTHORITY_AND_FAIL_CLOSED_BOUNDARIES]]
- [[26_VERSIONING_MIGRATION_AND_PACKAGE_RELEASE]]
- [[27_COMPILE_TEST_AND_RELEASE_RUNBOOK]]
- [[28_ACCEPTANCE_EVIDENCE_LIMITATIONS_AND_RESIDUAL_RISK]]
- [[29_HANDOFF_TO_UCE_I03_TREATMENT_ATOM_REGISTRIES]]
- [[30_FIELD_LEVEL_DATA_DICTIONARY]]

## Architectural Invariants

1. Context truth ends before treatment choice.
2. Every context occurrence has one stable identity and an explicit known-time chain.
3. Every feature declares owner, type, units, shape, missingness, staleness, dependencies, first-known semantics, runtime availability, and export capability.
4. Every representation view shares the same context occurrence identity and feature-frame lineage.
5. Every dependence structure required by splitting, statistics, and treatment siblings is explicit.
6. Manual setups remain first-class package attachments and require no model.
7. Research, Strategy Tester, paper, shadow, and live modes consume the same semantics or abstain.
8. No package can send, check, modify, or manage broker orders.

## Produced Modules

```text
strategy_factory_contexts_v3/
ContextPackage/
  UCE02_Manifest
  UCE02_Observation
  UCE02_Lifecycle
  UCE02_Feature
  UCE02_Representation
  UCE02_Cluster
  UCE02_ContextPackage
  UCE02_Registry
  UCE02_ReferenceSynthetic
  UCE02_EXP0017Reference
  UCE02_Conformance
```

## Source Architecture

- [[05_CONTEXT_CONTRACT_AND_CONTEXT_SDK]]
- [[14_FEATURE_ENGINEERING_AND_REPRESENTATION]]
- [[CON_02_CONTEXT_OBSERVATION_LIFECYCLE]]
- [[CON_03_FEATURE_DESCRIPTOR_AVAILABILITY]]
- [[CON_04_REPRESENTATION_VIEW]]
- [[UCE_I01_CANONICAL_CONTRACTS_AND_IDENTITY_KERNEL]]
