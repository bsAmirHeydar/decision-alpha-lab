---
title: "UCE-I07 — Universal Trainer SDK, Capability Registry, and Task Orchestrator"
tags: [strategy-factory, ucee, trainer-sdk, task-orchestrator, moc]
status: implemented
doc_version: 1.0.0
last_updated: 2026-07-12
---
# UCE-I07 — Universal Trainer SDK, Capability Registry, and Task Orchestrator

## Mission

UCE-I07 establishes the universal, task-aware training control plane that accepts an immutable UCE-I06 dataset release and runs any compatible trainer through the same causal folds, guarded data roles, deterministic budgets, lineage protocol, artifact contract, and failure ledger. It is the stable seam between context research and the algorithm packs introduced in UCE-I08 through UCE-I10.

## Core result

```text
Immutable Dataset Release
  → Task Contract
  → Exact Trainer Capability Match
  → Fold-local Fit / Calibration / Threshold / OOF
  → Selection Lock
  → Final Refit
  → One-shot Final Test
  → Model State + Manifest + Model Card + Full Trial Ledger
```

## Navigation

- [[01_PHASE_CHARTER_AND_NON_NEGOTIABLES]]
- [[02_ARCHITECTURE_AUTHORITY_AND_TRUST_BOUNDARIES]]
- [[03_CANONICAL_TRAINER_CAPABILITY_DESCRIPTOR]]
- [[04_EXACT_VERSION_REGISTRY_AND_PLUGIN_DISCOVERY]]
- [[05_TRAINER_LIFECYCLE_STATE_MACHINE]]
- [[06_TASK_TAXONOMY_AND_COMPATIBILITY_ROUTING]]
- [[07_GUARDED_DATASET_VIEWS_AND_FINAL_TEST_SEAL]]
- [[08_FOLD_LOCAL_OOF_PROTOCOL]]
- [[09_CALIBRATION_THRESHOLD_AND_DECISION_SEPARATION]]
- [[10_FINAL_MODEL_REFIT_AND_ONE_SHOT_TEST_EVALUATION]]
- [[11_RESOURCE_BUDGETS_AND_ADMISSION_CONTROL]]
- [[12_DETERMINISM_REPRODUCIBILITY_AND_NUMERIC_TOLERANCE]]
- [[13_CANCELLATION_TIMEOUT_CHECKPOINT_AND_RESTART]]
- [[14_PREDICTION_LINEAGE_AND_ACCESS_AUDIT]]
- [[15_TRIAL_LEDGER_FAILURE_AND_PRUNING_RETENTION]]
- [[16_MODEL_STATE_SERIALIZATION_AND_PARITY]]
- [[17_ARTIFACT_MANIFEST_AND_RELEASE_EVIDENCE]]
- [[18_MODEL_CARD_LIMITATIONS_AND_RISK_DISCLOSURE]]
- [[19_METRICS_CALIBRATION_EXPLAINABILITY_AND_TASK_OUTPUTS]]
- [[20_REFERENCE_PRIOR_BINARY_TRAINER]]
- [[21_REFERENCE_MEAN_REGRESSION_TRAINER]]
- [[22_REFERENCE_LINEAR_RANKING_TRAINER]]
- [[23_SHARED_CONFORMANCE_SUITE_AND_GOLDEN_VECTORS]]
- [[24_NEGATIVE_CHAOS_AND_RESOURCE_PRESSURE_TESTS]]
- [[25_MQL5_CONTRACT_PARITY_AND_RUNTIME_BOUNDARY]]
- [[26_TELEMETRY_OBSERVABILITY_AND_FAILURE_CODES]]
- [[27_SECURITY_SUPPLY_CHAIN_AND_UNTRUSTED_ARTIFACTS]]
- [[28_MIGRATION_FROM_SF13_SF14_AND_UCE_I06]]
- [[29_SCALE_OUT_CACHING_AND_DISTRIBUTED_EXECUTION_BOUNDARY]]
- [[30_ACCEPTANCE_EVIDENCE_LIMITATIONS_AND_RESIDUAL_RISKS]]
- [[31_HANDOFF_TO_UCE_I08_CLASSICAL_TABULAR_ALGORITHMS]]
- [[ADRs/ADR_001_EXACT_VERSION_RESOLUTION_ONLY]]
- [[ADRs/ADR_002_FINAL_TEST_IS_SEALED]]
- [[ADRs/ADR_003_FAILED_TRIALS_ARE_FIRST_CLASS_EVIDENCE]]
- [[ADRs/ADR_004_REFERENCE_TRAINERS_ARE_CONFORMANCE_ORACLES]]
- [[ADRs/ADR_005_NO_OPAQUE_PICKLE_AS_CANONICAL_STATE]]

## Machine-readable surfaces

- `strategy_factory_trainers_v3` — reference Python SDK and orchestrator.
- `TrainerSDK/UCEI07_*` — MQL5 contract and conformance mirror.
- closed JSON schemas under `schemas/v3`.
- three trainer-family golden vectors and negative capability vectors.
- phase status, acceptance evidence, artifact inventory, QA, and handoff records.

## Authority statement

UCE-I07 may read governed research datasets and produce model evidence. It has no market-data authority, no treatment-generation authority, no model-promotion authority, no inference authority, and no live order authority.
