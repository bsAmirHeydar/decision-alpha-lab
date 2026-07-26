---
title: "UCE-I10 — Deep Multi-View, Graph, and Regime Pack"
tags: [strategy-factory, universal-context-engine, uce-i10, implementation-delivery]
status: implemented_python_and_static_validated
phase_version: 1.1.0
doc_version: 1.1.0
last_updated: 2026-07-13
---
# UCE-I10 — Deep Multi-View, Graph, and Regime Pack

## Decision summary

UCE-I10 introduces a **contract-first, fail-closed deep representation and qualification layer** after Context and the accepted classical/advanced task packs. It deliberately separates five things that are often conflated: representation construction, model fitting, evidence qualification, runtime export, and trading authority. This phase implements the first four as research contracts and native deterministic references. It grants **no order authority**.

## Completion boundary

| Area | Delivered | Status |
|---|---|---|
| Sequence | causal windows, masks, deterministic temporal reference, adapters | implemented |
| Raster/Vision | reproducible renderer, pixel audit, deterministic visual reference | implemented |
| Graph | topology lineage, canonical edges, message-passing reference | implemented |
| Regime/Novelty | deterministic states, transitions, CUSUM, novelty, expert gate | implemented |
| Fusion | late, gated and OOF stacked fusion, missing-view policies | implemented |
| Transfer/Compression | leakage boundary, distillation, int8 quantization | implemented |
| Qualification | admission, multi-seed, ablation, export/parity/latency gates | implemented |
| Trainer SDK | five native trainers registered under exact capabilities | implemented |
| MQL5 | contract mirror, diagnostic and static self-tests | static validated; MetaEditor compile pending local Windows |
| Execution | broker/order/position authority | explicitly absent |

## Architecture flow

```text
ContextObservation + known_time
        │
        ├─ SequenceWindowBuilder ──> SequenceArtifact
        ├─ ChartRasterRenderer ────> RasterArtifact + PixelAudit
        ├─ GraphBuilder ───────────> GraphArtifact + TopologyHash
        └─ Regime/Novelty ─────────> Routing Evidence
                         │
             Native baselines / optional adapters
                         │
                  OOF base predictions
                         │
           Late / Gated / OOF-Stacked Fusion
                         │
     Multi-seed + economics + calibration + ablation
                         │
           Export parity + latency + fallback proof
                         │
        PROMOTABLE / CHALLENGER_ONLY / REJECTED
```

## Normative chapter map

- [[01_MISSION_SCOPE_AND_NON_GOALS|UCE-I10 Mission, Scope, and Non-Goals]]
- [[02_DEEP_ADMISSION_AND_CLASSICAL_GATE|Deep Admission and Classical Gate]]
- [[03_SEQUENCE_CONTRACTS_CAUSAL_MASKS_AND_WINDOWS|Sequence Contracts, Causal Masks, and Windows]]
- [[04_SEQUENCE_ENCODERS_AND_ADAPTER_BOUNDARIES|Sequence Encoders and Adapter Boundaries]]
- [[05_DETERMINISTIC_CHART_RASTER_AND_PIXEL_AUDIT|Deterministic Chart Raster and Pixel Audit]]
- [[06_VISION_ADAPTERS_AND_AUGMENTATION_RESTRICTIONS|Vision Adapters and Augmentation Restrictions]]
- [[07_GRAPH_TOPOLOGY_LINEAGE_AND_MESSAGE_PASSING|Graph Topology, Lineage, and Message Passing]]
- [[08_GRAPH_BASELINES_BATCHING_AND_ABLATIONS|Graph Baselines, Batching, and Ablations]]
- [[09_REGIME_STATE_CHANGE_POINT_AND_NOVELTY|Regime, State, Change-Point, and Novelty]]
- [[10_REGIME_EXPERT_FALLBACK_AND_ABSTENTION|Regime Expert Fallback and Abstention]]
- [[11_MULTI_VIEW_FUSION_AND_MISSING_VIEW_POLICY|Multi-View Fusion and Missing-View Policy]]
- [[12_STACKING_GATED_FUSION_AND_CROSS_ATTENTION_GATE|Stacking, Gated Fusion, and Cross-Attention Gate]]
- [[13_TRANSFER_PRETRAINING_AND_FINE_TUNING_BOUNDARIES|Transfer, Pretraining, and Fine-Tuning Boundaries]]
- [[14_DISTILLATION_QUANTIZATION_AND_COMPRESSION|Distillation, Quantization, and Compression]]
- [[15_DEEP_QUALIFICATION_MULTI_SEED_AND_EXPORT|Deep Qualification, Multi-Seed Stability, and Export]]
- [[16_TRAINER_SDK_INTEGRATION_AND_CAPABILITY_FLAGS|Trainer SDK Integration and Capability Flags]]
- [[17_DETERMINISM_RESOURCE_AND_SERIALIZATION_POLICY|Determinism, Resource, and Serialization Policy]]
- [[18_MQL5_RUNTIME_CONTRACT_BOUNDARY|MQL5 Runtime Contract Boundary]]
- [[19_TEST_STRATEGY_GOLDEN_NEGATIVE_AND_CHAOS|Test Strategy: Golden, Negative, and Chaos]]
- [[20_FAILURE_MODES_RESIDUAL_RISKS_AND_HANDOFF|Failure Modes, Residual Risks, and UCE-I11 Handoff]]
- [[21_OPERATOR_RUNBOOK|UCE-I10 Operator Runbook]]
- [[22_ACCEPTANCE_EVIDENCE|UCE-I10 Acceptance Evidence]]
- [[23_CODE_SURFACE_AND_API_REFERENCE|Code Surface and API Reference]]
- [[24_SCHEMA_CATALOG_AND_VERSIONING|Schema Catalog and Versioning]]
- [[25_EXPERIMENT_EXAMPLES_AND_EXPECTED_EVIDENCE|Experiment Examples and Expected Evidence]]
- [[26_PATCH_EXPAND_REMOVE_COMMIT_PUSH_RUNBOOK|Patch, Expand, Remove-ZIP, Commit, and Push Runbook]]

## ADRs

- [[adrs/ADR_I10_001_DEEP_ADMISSION_IS_NON_BYPASSABLE]]
- [[adrs/ADR_I10_002_VIEW_KNOWN_TIME_IS_PART_OF_IDENTITY]]
- [[adrs/ADR_I10_003_CROSS_ATTENTION_REQUIRES_LATE_FUSION_EVIDENCE]]

## Implementation inventory

| Surface | Path |
|---|---|
| Python package | `lab/11_strategy_factory/python/strategy_factory_deep_views_v3` |
| Python tests | `lab/11_strategy_factory/tests/phase_uce_i10_deep_views` |
| JSON schemas | `lab/11_strategy_factory/schemas/v3` |
| Test vectors | `lab/11_strategy_factory/test_vectors/v3/uce_i10_deep_view_conformance_vectors.json` |
| MQL5 contracts | `mql5/Include/AlphaLab/StrategyFactory/DeepViews` |
| MQL5 diagnostics | `mql5/Experts/StrategyFactory` and `mql5/Experts/StrategyFactoryTests` |
| Phase evidence | `lab/11_strategy_factory/phase_status` and repository-root I10 manifests |
| Tools | `tools/strategy_factory/*uce_i10*` |

## Golden acceptance chain

1. Deep admission proves sufficient independent support, causal views, stable dimensions, and an accepted classical floor.
2. Every representation passes deterministic replay and future-perturbation checks where applicable.
3. Native and optional candidates use the same dataset/fold/target/economic contracts.
4. At least three unique seeds are evaluated and failed runs remain in the report.
5. Every view has an ablation; fusion candidates use OOF base predictions.
6. A promotable candidate has an approved export path, parity, latency, and fallback evidence.
7. The final-test set remains sealed until the candidate and policy are frozen.

## First UCE-I11 golden test

Given the same admitted candidate set, dataset manifest, fold plan, seed set, budget, and scheduler version, UCE-I11 must emit the identical experiment DAG and trial identities. A rejected I10 candidate must never enter the DAG.

## Navigation

- [[../../phases/UCE_I10_DEEP_MULTI_VIEW_GRAPH_AND_REGIME_PACK|Canonical phase specification]]
- [[../../phases/UCE_I11_EXPERIMENT_DAG_SEARCH_AND_BUDGETING|Next phase: UCE-I11]]
- [[../../../00_UCEE_MASTER_MOC|UCEE master MOC]]
