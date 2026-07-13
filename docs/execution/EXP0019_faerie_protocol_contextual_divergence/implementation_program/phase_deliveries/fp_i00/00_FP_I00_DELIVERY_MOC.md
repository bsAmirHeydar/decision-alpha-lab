---
title: "FP-I00 — Governance, Baseline Freeze, and Source-Control Harness"
tags: [exp0019, faerie-protocol, fp-i00, governance, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I00
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---

# FP-I00 — Governance, Baseline Freeze, and Source-Control Harness

## Executive decision

FP-I00 is implemented as an executable governance phase. It freezes the authoritative Faerie Protocol source, owner decisions, open decision, relation registry, implementation program, documentation tree, shared-core dependencies, previous-context regression entry points, file ownership, authority boundary, and rollback semantics before any MQL5 Faerie Protocol runtime code exists.

## Phase health model

```text
READY     no blocking issue and no warning
DEGRADED  no blocking issue, but operator review is required
BLOCKED   at least one required contract, dependency, test, authority, ownership, or manifest check failed
```

## Product boundary

| Surface | FP-I00 status |
|---|---|
| Faerie Protocol detector | forbidden |
| Context engine | forbidden |
| Indicator | forbidden |
| Diagnostic EA | forbidden |
| Paper execution | forbidden |
| Live execution | forbidden and additionally blocked by FP-DEC-012 |
| Governance tooling | implemented |
| Documentation and evidence | implemented |

## Executable outputs

- `FP_I00_BASELINE_MANIFEST.v1.json`
- `FP_I00_SHARED_CORE_DEPENDENCY_INVENTORY.csv/json`
- `FP_I00_PREVIOUS_CONTEXT_TEST_INVENTORY.csv`
- `FP_I00_PHASE_FILE_OWNERSHIP.csv`
- `FP_I00_VALIDATION_REPORT.json`

## Validation command

```powershell
& .\lab_infrastructure\EXP0019_faerie_protocol\phase_i00\powershellun_exp0019_fp_i00_checks.ps1 -RepoRoot .
```

## Chapter map
- [[01_PHASE_CHARTER_AUTHORITY_AND_NON_GOALS|Phase Charter, Authority, and Non-Goals]]
- [[02_BASELINE_MANIFEST_MODEL_AND_IDENTITY|Baseline Manifest Model and Identity]]
- [[03_SOURCE_CONTROL_CAPTURE_AND_PHASE_CLEANLINESS|Source-Control Capture and Phase Cleanliness]]
- [[04_EXTERNAL_SOURCE_PACKAGE_FREEZE|External Source Package Freeze]]
- [[05_DOCUMENTATION_AND_NORMATIVE_BASELINE_FREEZE|Documentation and Normative Baseline Freeze]]
- [[06_OWNER_DECISION_FREEZE_AND_OPEN_DECISION_GATE|Owner Decision Freeze and Open-Decision Gate]]
- [[07_RELATION_AND_PROGRAM_REGISTRY_FREEZE|Relation and Program Registry Freeze]]
- [[08_SHARED_CORE_DEPENDENCY_INVENTORY|Shared-Core Dependency Inventory]]
- [[09_REUSE_CLASSIFICATION_AND_NO_FORK_POLICY|Reuse Classification and No-Fork Policy]]
- [[10_PREVIOUS_CONTEXT_COMPATIBILITY_TEST_CATALOG|Previous-Context Compatibility Test Catalog]]
- [[11_PHASE_FILE_OWNERSHIP_PATCH_AND_ROLLBACK|Phase File Ownership, Patch Scope, and Rollback]]
- [[12_VERSIONING_REBASELINE_AND_CHANGE_CONTROL|Versioning, Rebaseline, and Change Control]]
- [[13_GOVERNANCE_HARNESS_ARCHITECTURE_AND_API|Governance Harness Architecture and API]]
- [[14_REASON_CODES_FAILURE_MODES_AND_FAIL_CLOSED_BEHAVIOR|Reason Codes, Failure Modes, and Fail-Closed Behavior]]
- [[15_TEST_STRATEGY_FIXTURES_AND_NEGATIVE_CASES|Test Strategy, Fixtures, and Negative Cases]]
- [[16_OPERATOR_RUNBOOK_AND_LOCAL_ACCEPTANCE|Operator Runbook and Local Acceptance]]
- [[17_ACCEPTANCE_EVIDENCE_QA_AND_AUDIT_PACKAGE|Acceptance Evidence, QA, and Audit Package]]
- [[18_HANDOFF_TO_FP_I01_COMPATIBILITY_HARNESS|Handoff to FP-I01 Compatibility Harness]]
- [[19_ROLLBACK_RECOVERY_AND_INCIDENT_RESPONSE|Rollback, Recovery, and Incident Response]]
- [[20_CODE_FILE_AND_ARTIFACT_CATALOG|Code, File, and Artifact Catalog]]


## ADR map

- [[adrs/ADR_FP_I00_001_NO_RUNTIME_CODE_IN_GOVERNANCE_PHASE]]
- [[adrs/ADR_FP_I00_002_HASH_PIN_SHARED_DEPENDENCIES]]
- [[adrs/ADR_FP_I00_003_PHASE_CLEANLINESS_EXCLUDES_OWNED_PATCH_FILES]]
- [[adrs/ADR_FP_I00_004_FP_DEC_012_BLOCKS_LIVE_EXECUTION]]
- [[adrs/ADR_FP_I00_005_SHARED_CORES_ARE_READ_ONLY_INPUTS]]
- [[adrs/ADR_FP_I00_006_FILE_INDEX_IS_ROLLBACK_BOUNDARY]]

## Acceptance summary

- Frozen source artifacts: **3**
- Owner decisions: **15**
- Open decisions: **1 (`FP-DEC-012`)**
- Relations: **7**
- Implementation phases: **17**
- Shared dependency records: **19**
- Previous-context test records: **12**
- FP-I00 Python tests: **26**
- Governance checks in golden repository: **139**
- Runtime authority: **none**

## Navigation

- [[../../00_IMPLEMENTATION_PROGRAM_MOC|Implementation Program MOC]]
- [[../../phases/FP_I00_GOVERNANCE_BASELINE_FREEZE_AND_SOURCE-CONTROL_HARNESS|Canonical phase plan]]
- [[../../phases/FP_I01_SHARED-CORE_COMPATIBILITY_HARNESS_AND_ADAPTER_CONTRACTS|Next phase — FP-I01]]
- [[../../../00_EXP0019_MOC|EXP0019 Master MOC]]
