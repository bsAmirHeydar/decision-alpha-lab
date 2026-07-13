---
title: "UCE-I11 — Experiment DAG, Search, Scheduling, and Budget Governance"
tags: [strategy-factory, universal-context-engine, uce-i11, implementation-delivery]
status: implemented_python_and_static_validated
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
---
# UCE-I11 — Experiment DAG, Search, Scheduling, and Budget Governance

## Decision summary

UCE-I11 converts immutable datasets, folds, targets, economics, known-time policies, UCE-I10 candidate admissions, trainer keys, search spaces, seeds, calibration/threshold axes, resource estimates, and export requirements into a **deterministic, resumable, budgeted experiment DAG**. It does not decide that a strategy has edge and it does not grant trading authority. Its job is to make the full attempted search universe observable and reproducible before UCE-I12 applies multiplicity-aware statistical promotion.

## Completion boundary

| Area | Delivered | Status |
|---|---|---|
| Manifest compiler | exact declaration, nodes, edges, trials, claims, hashes | implemented |
| Candidate admission | accept/warn scheduling; reject evidence-only | implemented |
| Search | baseline, grid, random, Halton, TPE reference, halving, Hyperband, evolutionary, Pareto, Optuna boundary | implemented |
| Budget | trial, candidate, wall, memory, CPU/GPU, retry, artifact, seed, fold ceilings | implemented |
| Scheduler | dependency ordering, priority, events, retry, cancel, timeout, quarantine, cache, resume | implemented |
| Isolation | spawn-based local process boundary and environment capture | implemented |
| Ledger | append-only hash chain for all outcomes and overrides | implemented |
| Cache | content-addressed producer/schema/input/provenance validation | implemented |
| Reproducibility | semantic manifest, counts, selection, events, artifact tolerance | implemented |
| MQL5 | contract mirror, registry, budget guard, diagnostics/self-tests | static validated; MetaEditor pending local Windows |
| Execution | broker/order/position/network authority | explicitly absent |

## Architecture flow

```text
UCE-I10 admission evidence + immutable dataset/split/target/economics contracts
                              │
                    ExperimentDeclaration
                              │
                    ExperimentDagCompiler
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
 exact TrialIdentity     ResourceClaim        DAG nodes/edges
        │                     │                     │
        └─────────────────────┴──────────┬──────────┘
                                        │
                         DeterministicScheduler
                 ready → claim → isolate → run → evidence
                                        │
             ┌──────────────┬───────────┼──────────────┐
             │              │           │              │
        BudgetUsage    SchedulerEvents  SelectionLedger  ContentCache
             └──────────────┴───────────┴──────────────┘
                                        │
                         ReproducibilityReport
                                        │
                 UCE-I12 statistical/anti-overfit gate
```

## Golden acceptance chain

1. Rejected UCE-I10 candidates remain evidence and never enter the DAG.
2. The protected final-test role is absent from requested search roles.
3. The same declaration emits identical nodes, edges, trial IDs, claims, and manifest hash.
4. Baselines are ordered before challengers.
5. Trial and resource multiplicity is cut off only by explicit budget policy.
6. Retry, cancellation, timeout, quarantine, cache, and resume are event/ledger evidence.
7. Declared and executed trial counts reconcile.
8. Selected trial sets, event streams, and artifacts reproduce within declared tolerance.
9. Every model in a report exists as selected or ensembled in the ledger.
10. No runtime trading authority exists.

## Implementation inventory

| Surface | Path |
|---|---|
| Python package | `lab/11_strategy_factory/python/strategy_factory_experiments_v3` |
| Phase tests | `lab/11_strategy_factory/tests/phase_uce_i11_experiments` |
| Public schemas | `lab/11_strategy_factory/schemas/v3/experiment_*.schema.json` |
| Examples | `lab/11_strategy_factory/examples/uce_i11` |
| Vectors | `lab/11_strategy_factory/test_vectors/v3/uce_i11_experiment_conformance_vectors.json` |
| MQL5 contracts | `mql5/Include/AlphaLab/StrategyFactory/ExperimentOrchestration` |
| Tools | `tools/strategy_factory/*uce_i11*` |
| Status/evidence | `lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation` |

## Chapter map
- [[01_MISSION_SCOPE_AND_NON_GOALS|Mission, Scope, and Non-Goals]]
- [[02_ADMISSION_AND_BASELINE_FIRST_POLICY|Admission Boundary and Baseline-First Policy]]
- [[03_EXPERIMENT_DECLARATION_AND_IDENTITY|Experiment Declaration and Identity]]
- [[04_DAG_COMPILER_AND_NODE_TAXONOMY|DAG Compiler and Node Taxonomy]]
- [[05_DAG_DETERMINISM_TOPOLOGY_AND_PRIORITY|DAG Determinism, Topology, and Priority]]
- [[06_SEARCH_REGISTRY_AND_ADAPTER_CONTRACTS|Search Registry and Adapter Contracts]]
- [[07_GRID_RANDOM_AND_QUASI_RANDOM_SEARCH|Grid, Random, and Quasi-Random Search]]
- [[08_TPE_AND_BAYESIAN_ADAPTER_BOUNDARY|TPE and Bayesian Adapter Boundary]]
- [[09_SUCCESSIVE_HALVING_AND_HYPERBAND|Successive Halving and Hyperband]]
- [[10_EVOLUTIONARY_AND_MULTI_OBJECTIVE_SEARCH|Evolutionary and Multi-Objective Search]]
- [[11_BUDGET_HIERARCHY_AND_HARD_CUTOFFS|Budget Hierarchy and Hard Cutoffs]]
- [[12_RESOURCE_CLAIMS_AND_ENVIRONMENT_CAPTURE|Resource Claims and Environment Capture]]
- [[13_SCHEDULER_DEPENDENCY_EXECUTION_AND_EVENTS|Scheduler Dependency Execution and Events]]
- [[14_PROCESS_ISOLATION_RETRY_CANCEL_AND_QUARANTINE|Process Isolation, Retry, Cancellation, and Quarantine]]
- [[15_SELECTION_LEDGER_AND_MANUAL_OVERRIDE|Selection Ledger and Manual Override]]
- [[16_CONTENT_CACHE_PROVENANCE_AND_RESUME|Content Cache, Provenance, and Resume]]
- [[17_REPRODUCIBILITY_AUDIT_AND_RECONCILIATION|Reproducibility Audit and Reconciliation]]
- [[18_HIDDEN_FINAL_TEST_SEALING_AND_ANTI_LEAKAGE|Hidden Final-Test Sealing and Anti-Leakage]]
- [[19_TRAINER_SDK_AND_I10_INTEGRATION|Trainer SDK and UCE-I10 Integration]]
- [[20_MQL5_CONTRACT_MIRROR_AND_RUNTIME_BOUNDARY|MQL5 Contract Mirror and Runtime Boundary]]
- [[21_TELEMETRY_OPERATOR_RUNBOOK_AND_INCIDENTS|Telemetry, Operator Runbook, and Incidents]]
- [[22_TEST_STRATEGY_GOLDEN_NEGATIVE_AND_CHAOS|Test Strategy: Golden, Negative, and Chaos]]
- [[23_FAILURE_MODES_RESIDUAL_RISKS_AND_ROLLBACK|Failure Modes, Residual Risks, and Rollback]]
- [[24_ACCEPTANCE_EVIDENCE_AND_GATE_MATRIX|Acceptance Evidence and Gate Matrix]]
- [[25_CODE_API_AND_SCHEMA_CATALOG|Code, API, and Schema Catalog]]
- [[26_EXPERIMENT_PLAYBOOKS_AND_EXPECTED_ARTIFACTS|Experiment Playbooks and Expected Artifacts]]
- [[27_PATCH_EXPAND_REMOVE_COMMIT_PUSH_RUNBOOK|Patch, Expand, Remove-ZIP, Commit, and Push Runbook]]


## ADRs

- [[adrs/ADR_I11_001_COMPILED_MANIFEST_IS_IMMUTABLE]]
- [[adrs/ADR_I11_002_REJECTED_CANDIDATES_ARE_EVIDENCE_ONLY]]
- [[adrs/ADR_I11_003_BUDGETS_FAIL_CLOSED]]
- [[adrs/ADR_I11_004_CACHE_IDENTITY_INCLUDES_PROVENANCE]]

## First UCE-I12 golden test

Given the complete I11 selection ledger and immutable trial universe, UCE-I12 must count every attempted, skipped, pruned, failed, timed-out, selected, and overridden choice in its family/multiplicity evidence. A strong winner metric may not erase search breadth or a critical leakage/integrity blocker.

## Navigation

- [[../../phases/UCE_I11_EXPERIMENT_DAG_SEARCH_AND_BUDGETING|Canonical UCE-I11 phase specification]]
- [[../../phases/UCE_I12_STATISTICAL_AND_ANTI_OVERFIT_PROMOTION_GATE|Next phase: UCE-I12]]
- [[../../../00_UCEE_MASTER_MOC|UCEE master MOC]]
