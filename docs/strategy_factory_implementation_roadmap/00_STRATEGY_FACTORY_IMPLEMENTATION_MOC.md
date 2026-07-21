---
title: "Strategy Factory Implementation Program — Master MOC"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Strategy Factory Implementation Program — Master MOC

## Mission

Implement a durable, modular, low-latency platform that converts any deterministic or semi-deterministic market anatomy into reproducible research, candidate execution policies, anti-overfit validation, trained decision models, paper execution, and controlled live execution.

The implementation target is not one strategy. It is a reusable **Alpha Production Platform**.

```text
Anatomy
→ Canonical Event
→ Causal Context
→ Candidate Action Space
→ Outcome Simulation
→ Statistics and Nulls
→ Anti-Overfit Validation
→ Model Training and Ranking
→ Compiled Decision Runtime
→ Risk and Portfolio Governance
→ Paper Execution
→ Broker Execution
→ Monitoring and Promotion
```

## Program Rules

1. **Kernel before strategy customization.**
2. **Contracts before implementations.**
3. **Research path and live fast path remain separate.**
4. **No live order authority until paper parity and safety gates pass.**
5. **Every phase has tests, artifacts, and a kill condition.**
6. **No phase is accepted because code compiles; it is accepted because its contract is proven.**
7. **New strategy meanings remain plugins. Shared mechanics remain in the platform.**

## Execution Order

| Wave | Phases | Goal |
|---|---|---|
| Foundation | 00–05 | Freeze contracts, repository boundaries, package skeleton, plugin kernel, compiler |
| Research Engine | 06–12 | Context, features, candidates, simulation, statistics, anti-overfit |
| Intelligence | 13–15 | Training, registry, compiled decision runtime |
| Capital Boundary | 16–19 | Portfolio risk, paper execution, MQL5 bridge, monitoring |
| Proof and Migration | 20–24 | Pilot, second strategy, migration, hardening, release |

## Primary Documents

- [[01_PROGRAM_CHARTER]]
- [[02_TARGET_ARCHITECTURE]]
- [[03_PHASE_DEPENDENCY_GRAPH]]
- [[04_REPOSITORY_AND_MODULE_MAP]]
- [[05_CANONICAL_CONTRACT_FREEZE]]
- [[06_TESTING_AND_QUALITY_MASTER_PLAN]]
- [[07_ANTI_OVERFIT_IMPLEMENTATION_PLAN]]
- [[08_LOW_LATENCY_IMPLEMENTATION_PLAN]]
- [[09_SECURITY_SAFETY_AND_CAPITAL_BOUNDARY]]
- [[10_MIGRATION_AND_COMPATIBILITY_PLAN]]
- [[docs/evidence/release_versioning_plan/aa54c1fa30e1_11_RELEASE_AND_VERSIONING_PLAN]]
- [[12_PROGRAM_GOVERNANCE_AND_COMMIT_PROTOCOL]]

## Phase Documents

- [[phases/PHASE_00_CURRENT_STATE_AUDIT]]
- [[phases/PHASE_01_CONTRACTS_AND_SCHEMA]]
- [[phases/PHASE_02_PACKAGE_SKELETON_AND_BOUNDARIES]]
- [[phases/PHASE_03_PLUGIN_KERNEL_AND_CAPABILITIES]]
- [[phases/PHASE_04_MANIFEST_SCHEMA_AND_COMPILER]]
- [[phases/PHASE_05_ARTIFACT_IDENTITY_AND_REPRODUCIBILITY]]
- [[phases/PHASE_06_ANATOMY_ADAPTER_SDK]]
- [[phases/PHASE_07_CONTEXT_STATE_AND_MARKET_CLOCK]]
- [[phases/PHASE_08_FEATURE_DAG_AND_INCREMENTAL_CACHE]]
- [[phases/PHASE_09_CANDIDATE_POLICY_ENGINE]]
- [[phases/PHASE_10_OUTCOME_SIMULATOR_AND_COSTS]]
- [[phases/PHASE_11_STATISTICS_REPORTING_AND_NULLS]]
- [[phases/PHASE_12_ANTI_OVERFIT_VALIDATION_ENGINE]]
- [[phases/PHASE_13_TRAINING_PIPELINE_AND_BASELINES]]
- [[phases/PHASE_14_MODEL_REGISTRY_AND_PROMOTION]]
- [[phases/PHASE_15_COMPILED_DECISION_RUNTIME]]
- [[phases/PHASE_16_PORTFOLIO_RISK_AND_ACTION_PLANS]]
- [[phases/PHASE_17_PAPER_BROKER_AND_REPLAY]]
- [[phases/PHASE_18_MQL5_RUNTIME_AND_BROKER_BOUNDARY]]
- [[phases/PHASE_19_OBSERVABILITY_LATENCY_AND_DRIFT]]
- [[phases/PHASE_20_EXP0017_PILOT_INTEGRATION]]
- [[phases/PHASE_21_NDS_ZONE_AF_PILOT]]
- [[phases/PHASE_22_MULTI_STRATEGY_PORTFOLIO_LAYER]]
- [[phases/PHASE_23_PRODUCTION_HARDENING_AND_CHAOS_TESTS]]
- [[docs/evidence/phase_24_release_operating_model/2a81f79fd69e_PHASE_24_V1_RELEASE_AND_OPERATING_MODEL]]

## Operational Templates

- [[templates/NEW_PHASE_WORK_PACKET_TEMPLATE]]
- [[templates/NEW_PLUGIN_IMPLEMENTATION_TEMPLATE]]
- [[templates/NEW_STRATEGY_ONBOARDING_TEMPLATE]]
- [[templates/TEST_PLAN_TEMPLATE]]
- [[templates/ADR_TEMPLATE]]
- [[templates/MODEL_CARD_TEMPLATE]]
- [[templates/PROMOTION_DECISION_TEMPLATE]]
- [[templates/INCIDENT_POSTMORTEM_TEMPLATE]]

## Fastest Safe Path

The shortest path to a useful platform is:

```text
Phase 00 → 01 → 02 → 03 → 04 → 06 → 07 → 08 → 09 → 10
→ 11 → 12 → 13 → 15 → 17 → 20
```

This produces a complete **research-to-paper loop** for EXP0017 before live execution is touched.
