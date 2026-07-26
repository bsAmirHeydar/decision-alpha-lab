---
title: "FP-I01 — Shared-Core Compatibility Harness and Adapter Contracts"
tags: [exp0019, faerie-protocol, fp-i01, compatibility, adapter-contracts]
status: normative
phase: FP-I01
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---

# FP-I01 — Shared-Core Compatibility Harness and Adapter Contracts

## Decision summary

FP-I01 establishes the only permitted integration boundary between Faerie Protocol and the already accepted divergence infrastructure. Existing EXP0017, EXP0018, and Strategy Factory modules remain immutable semantic owners. Faerie Protocol receives read-only snapshots through exact-version adapters, converts them into neutral compatibility contracts, and records a source fingerprint for every projection.

The phase deliberately does **not** implement A/L/N sessions, Faerie relations, WW logic, indicator rendering, signal eligibility, risk, or execution. Those features remain downstream. This phase exists to prevent duplicated time/hunt/confirmation code and to prove that introducing Faerie adapters does not alter previous contexts.

## Delivered architecture

```text
EXP0017 / EXP0018 / Strategy Factory shared cores
                 │ immutable source snapshots
                 ▼
        Exact dependency hash guard
                 │
                 ▼
       Read-only versioned adapters
                 │ source fingerprint retained
                 ▼
    Neutral FP-I01 compatibility contracts
                 │
        ┌────────┴────────┐
        ▼                 ▼
 Golden differential   MQL5/Python parity
 evidence              contract mirror
```

## Hard invariants

1. Shared-core files are read-only inputs and are absent from the FP-I01 patch index.
2. Every dependency group must match its FP-I00 file count and aggregate SHA-256.
3. Every adapter has an exact key, explicit source type, explicit semantic delta, and no runtime authority.
4. Source payload hashes and deep values are unchanged after adaptation.
5. Identical source payloads produce identical neutral output hashes.
6. Missing or incompatible inputs are not guessed or defaulted into READY state.
7. EXP0017 and EXP0018 entry points remain discoverable and must compile locally before final acceptance.
8. FP-DEC-012 remains open and no execution semantics are inferred.

## Delivery metrics

| Surface | Delivered |
|---|---:|
| Python modules | 15 |
| Python tests | 39 |
| Dependency pins | 19 |
| Executable adapters | 8 |
| Golden fixtures | 8 |
| Previous-context test entry points | 12 |
| MQL5 contract headers | 9 |
| MQL5 diagnostic/self-test entry points | 2 |
| New Indicator/EA product logic | 0 |
| Broker/order/network authority | 0 |

## Chapter map
- [[01_PHASE_MISSION_SCOPE_AND_NON_GOALS|Phase Mission, Scope, and Non-Goals]]
- [[02_SHARED_CORE_ARCHITECTURE_AND_OWNERSHIP|Shared-Core Architecture and Ownership]]
- [[03_DEPENDENCY_PINNING_AND_VERSION_RESOLUTION|Dependency Pinning and Version Resolution]]
- [[04_REUSE_CLASSIFICATION_MATRIX|Reuse Classification Matrix]]
- [[05_NEUTRAL_COMPATIBILITY_CONTRACT_MODEL|Neutral Compatibility Contract Model]]
- [[06_TIME_ADAPTER_CONTRACT|Time Adapter Contract]]
- [[07_REFERENCE_ADAPTER_CONTRACT|Reference Adapter Contract]]
- [[08_HUNT_ADAPTER_CONTRACT|Hunt Adapter Contract]]
- [[09_DIVERGENCE_ADAPTER_CONTRACT|Divergence Adapter Contract]]
- [[10_CONFIRMATION_ADAPTER_CONTRACT|Confirmation Adapter Contract]]
- [[11_LIFECYCLE_ADAPTER_CONTRACT|Lifecycle Adapter Contract]]
- [[12_ADAPTER_REGISTRY_AND_EXACT_RESOLUTION|Adapter Registry and Exact Resolution]]
- [[13_READ_ONLY_AND_NON_MUTATION_PROOF|Read-Only and Non-Mutation Proof]]
- [[14_GOLDEN_FIXTURE_CATALOG|Golden Fixture Catalog]]
- [[15_DIFFERENTIAL_COMPATIBILITY_STRATEGY|Differential Compatibility Strategy]]
- [[16_PREVIOUS_CONTEXT_REGRESSION_BOUNDARY|Previous-Context Regression Boundary]]
- [[17_DUPLICATE_IMPLEMENTATION_AND_AUTHORITY_SCAN|Duplicate Implementation and Authority Scan]]
- [[18_HEALTH_REASON_CODES_AND_FAIL_CLOSED_BEHAVIOR|Health, Reason Codes, and Fail-Closed Behavior]]
- [[19_MQL5_CONTRACT_MIRROR|MQL5 Contract Mirror]]
- [[20_PYTHON_HARNESS_API_REFERENCE|Python Harness API Reference]]
- [[21_TEST_STRATEGY_GOLDEN_NEGATIVE_AND_STATIC|Test Strategy: Golden, Negative, and Static]]
- [[22_METAEDITOR_COMPILE_AND_LOCAL_RUNTIME_RUNBOOK|MetaEditor Compile and Local Runtime Runbook]]
- [[23_ARTIFACTS_REPORTS_AND_AUDIT_EVIDENCE|Artifacts, Reports, and Audit Evidence]]
- [[24_ROLLBACK_RECOVERY_AND_REBASE_POLICY|Rollback, Recovery, and Rebase Policy]]
- [[25_HANDOFF_TO_FP_I02|Handoff to FP-I02]]
- [[26_CODE_FILE_AND_SYMBOL_CATALOG|Code, File, and Symbol Catalog]]


## ADRs

- [[adrs/ADR_FP_I01_001_SHARED_CORES_REMAIN_SEMANTIC_OWNERS]]
- [[adrs/ADR_FP_I01_002_ADAPTERS_ARE_READ_ONLY_PROJECTIONS]]
- [[adrs/ADR_FP_I01_003_EXACT_HASH_PIN_BEFORE_ADAPTATION]]
- [[adrs/ADR_FP_I01_004_SOURCE_FINGERPRINT_SURVIVES_PROJECTION]]
- [[adrs/ADR_FP_I01_005_NEUTRAL_CONTRACTS_DO_NOT_DEFINE_FP_SEMANTICS]]
- [[adrs/ADR_FP_I01_006_METAEDITOR_IS_A_SEPARATE_ACCEPTANCE_GATE]]

## Acceptance command

```powershell
& .\lab_infrastructure\EXP0019_faerie_protocol\phase_i01\powershell
un_exp0019_fp_i01_checks.ps1 -RepoRoot $PWD
```

## Next phase

`FP-I02 — Core Context Types, Identity, and Reason-Code Kernel` owns native Faerie Protocol types and semantic IDs. It may consume the neutral contracts, but it may not reinterpret source fields or bypass exact dependency pins.

## Navigation

- [[../../00_IMPLEMENTATION_PROGRAM_MOC|Implementation Program MOC]]
- [[../../../00_EXP0019_MOC|EXP0019 Master MOC]]
- [[../fp_i00/00_FP_I00_DELIVERY_MOC|Previous phase: FP-I00]]
- [[../../phases/FP_I02_CORE_CONTEXT_TYPES_IDENTITY_AND_REASON_CODE_KERNEL|Next phase: FP-I02]]
