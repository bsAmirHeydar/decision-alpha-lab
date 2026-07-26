---
title: "FP-I02 — Core Context Types, Identity, and Reason-Code Kernel"
tags: [exp0019, faerie-protocol, fp-i02, contracts, identity, obsidian]
status: implemented_python_and_static_mql5_validated
phase: FP-I02
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# FP-I02 — Core Context Types, Identity, and Reason-Code Kernel

## Executive decision

FP-I02 freezes the public semantic vocabulary and object identity of Faerie Protocol before any time, data, reference, hunt, confirmation, WW, indicator, or execution engine is implemented. Every later phase must construct these records rather than invent parallel structs or IDs.

## Delivery summary

| Surface | Delivered |
|---|---|
| Python | 15 modules; immutable contracts, config, IDs, registries, state machines, validation, migration, conformance |
| JSON Schema | 18 closed Draft 2020-12 schemas |
| MQL5 | 11 include files, self-test EA, diagnostic EA |
| Registries | 7 relations, 35 reason codes, 16 public contracts, 4 state machines |
| Owner decisions | 14 frozen + FP-DEC-012 explicitly UNSET |
| Authority | NONE; live impossible |
| Next phase | FP-I03 exact New York time/session/week kernel |

## Architecture

```text
FP-I00 governance + FP-I01 read-only adapters
                    │
                    ▼
         SemanticConfiguration
         ProjectionConfiguration
         OperationalConfiguration
                    │
                    ▼
            ContextManifestRecord
                    │ context_epoch_id
       ┌────────────┼─────────────┐
       ▼            ▼             ▼
  Window/Ref     Hunt/Candidate  Signal/WW/Quota
       │            │             │
       └──────── canonical identities ────────┐
                                              ▼
                                 ledger/checkpoint/indicator
                                 in later phases only
```

## Chapter map
- [[01_PHASE_CHARTER_SCOPE_AUTHORITY_AND_NON_GOALS|Phase Charter, Scope, Authority, and Non-Goals]]
- [[02_PUBLIC_TYPE_SYSTEM_AND_CLOSED_ENUMS|Public Type System and Closed Enums]]
- [[03_SEMANTIC_PROJECTION_AND_OPERATIONAL_CONFIGURATION|Semantic, Projection, and Operational Configuration]]
- [[04_CONTEXT_MANIFEST_PROFILE_AND_AUTHORITY|Context Manifest, Profile, and Authority]]
- [[05_SYMBOL_PAIR_CONTRACT_AND_CANONICAL_ORDERING|Symbol Pair Contract and Canonical Ordering]]
- [[06_WINDOW_KEY_INTERVAL_AND_DATA_REVISION_IDENTITY|Window Key, Interval, and Data-Revision Identity]]
- [[07_WINDOW_RECORD_AND_COMPLETENESS_CONTRACT|Window Record and Completeness Contract]]
- [[08_REFERENCE_SIDE_KEY_AND_LIFECYCLE_RECORD|Reference-Side Key and Lifecycle Record]]
- [[09_HUNT_FACT_CONTRACT_AND_M1_AUTHORITY|Hunt Fact Contract and M1 Authority]]
- [[10_DIVERGENCE_CANDIDATE_CONTRACT|Divergence Candidate Contract]]
- [[11_CONFIRMATION_EVENT_AND_CONFIRMED_SIGNAL_CONTRACT|Confirmation Event and Confirmed Signal Contract]]
- [[12_WW_CONTEXT_RECORD_AND_RECENCY_LINEAGE|WW Context Record and Recency Lineage]]
- [[13_QUOTA_KEY_RECORD_AND_OPEN_CONSUMPTION_POLICY|Quota Key, Record, and Open Consumption Policy]]
- [[14_REASON_CODE_REGISTRY_AND_EVIDENCE|Reason-Code Registry and Evidence]]
- [[15_RELATION_REGISTRY_AND_REFERENCE_THEN_CHECK_NAMING|Relation Registry and Reference-Then-Check Naming]]
- [[16_CANONICAL_SERIALIZATION_HASHING_AND_COMPACT_IDS|Canonical Serialization, Hashing, and Compact IDs]]
- [[17_IDENTITY_DOMAINS_AND_FIELD_LEVEL_MATRICES|Identity Domains and Field-Level Matrices]]
- [[18_IDENTITY_LEDGER_DEDUPLICATION_AND_CONFLICTS|Identity Ledger, Deduplication, and Conflicts]]
- [[19_STATE_MACHINE_REGISTRY_AND_ILLEGAL_TRANSITIONS|State-Machine Registry and Illegal Transitions]]
- [[20_VALIDATION_REPORTS_AND_HEALTH_DERIVATION|Validation Reports and Health Derivation]]
- [[21_EXPLICIT_VERSIONING_AND_V1_TO_V2_MIGRATION|Explicit Versioning and v1-to-v2 Migration]]
- [[22_JSON_SCHEMA_CATALOG_AND_STRICT_WIRE_FORMATS|JSON Schema Catalog and Strict Wire Formats]]
- [[23_MQL5_CONTRACT_MIRROR_AND_CROSS_LANGUAGE_BOUNDARY|MQL5 Contract Mirror and Cross-Language Boundary]]
- [[24_FP_I01_ADAPTER_HANDOFF_AND_DEPENDENCY_SNAPSHOT|FP-I01 Adapter Handoff and Dependency Snapshot]]
- [[25_AUTHORITY_SECURITY_AND_FORBIDDEN_DEPENDENCIES|Authority, Security, and Forbidden Dependencies]]
- [[26_TEST_STRATEGY_GOLDEN_NEGATIVE_AND_PROPERTY_CHECKS|Test Strategy: Golden, Negative, and Property Checks]]
- [[27_GOLDEN_IDENTITY_VECTORS_AND_REPLAY_PARITY|Golden Identity Vectors and Replay Parity]]
- [[28_PERFORMANCE_MEMORY_AND_RESOURCE_BUDGETS|Performance, Memory, and Resource Budgets]]
- [[29_OPERATOR_RUNBOOK_AND_LOCAL_ACCEPTANCE|Operator Runbook and Local Acceptance]]
- [[30_COMPILE_TEST_PACKAGE_RELEASE_AND_ROLLBACK|Compile, Test, Package, Release, and Rollback]]
- [[31_OWNER_DECISION_TO_CONTRACT_TRACEABILITY|Owner Decision-to-Contract Traceability]]
- [[32_ACCEPTANCE_EVIDENCE_GATE_MATRIX_AND_RESIDUAL_RISK|Acceptance Evidence, Gate Matrix, and Residual Risk]]
- [[33_HANDOFF_TO_FP_I03_TIME_SESSION_AND_WEEK_KERNEL|Handoff to FP-I03 Time, Session, and Week Kernel]]
- [[34_CODE_API_ARTIFACT_AND_FILE_CATALOG|Code, API, Artifact, and File Catalog]]
- [[35_KNOWN_LIMITATIONS_AND_NON_CLAIMS|Known Limitations and Non-Claims]]


## ADRs

- [[adrs/ADR_FP_I02_001_SEMANTIC_AND_PROJECTION_IDENTITY_ARE_SEPARATE]]
- [[adrs/ADR_FP_I02_002_PUBLIC_ENUMS_ARE_CLOSED_AND_VERSIONED]]
- [[adrs/ADR_FP_I02_003_POLICY_OUTCOMES_DO_NOT_MUTATE_SIGNAL_ID]]
- [[adrs/ADR_FP_I02_004_DATA_REVISION_IS_IDENTITY_BEARING]]
- [[adrs/ADR_FP_I02_005_OPEN_DECISIONS_ARE_EXPLICIT_VALUES]]
- [[adrs/ADR_FP_I02_006_PUBLIC_REGISTRIES_ARE_FROZEN]]
- [[adrs/ADR_FP_I02_007_MQL5_IS_A_CONTRACT_MIRROR_NOT_A_SECOND_SEMANTIC_OWNER]]

## Contract reference

- [[contracts/FP_I02_PUBLIC_CONTRACT_REFERENCE]]
- [[contracts/FP_I02_IDENTITY_FIELD_MATRIX]]
- [[contracts/FP_I02_REASON_AND_STATE_REFERENCE]]

## Acceptance headline

The phase is accepted when Python tests and conformance pass, all public schemas validate, MQL5 static parity passes, FP-I00/I01 regressions remain green, engineering policy passes, and local MetaEditor logs are retained. In this environment MetaEditor remains `pending_local_windows`.
