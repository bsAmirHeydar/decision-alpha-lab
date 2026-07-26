---
title: "Research Telemetry"
phase: 10
status: canonical
tags: [strategy-factory, mql5, tester-research, phase10]
---
# Research Telemetry

Counts observations, rejections, sent and received frames, selected passes, export failures, differential mismatches and finalization latency.

## Design position

Phase 10 keeps the market, anatomy, candidate and outcome truth in MQL5. The research harness does not reinterpret a strategy. It aggregates canonical `SF09_OutcomeRecord` values, freezes exact lineage in `SF10_RunManifest`, calculates a conservative objective, and transports only compact pass evidence during optimization.

## Required invariants

1. Candidate and outcome identities never change during research.
2. A pass is invalid when its manifest, parameter hash, sample gate or metric reconciliation fails.
3. Optimization ranking is discovery evidence, not deployment authority.
4. Ambiguous or missing observations cannot improve the pass score.
5. Full event and path exports are produced only by selected reruns with explicit fidelity.
6. Every artifact is linked to generation, strategy, candidate matrix, simulation policy and cost model hashes.
7. No broker-order function belongs to this phase.

## Implementation modules

- `SF10_RunManifest.mqh` freezes complete run lineage.
- `SF10_ResearchMetrics.mqh` performs bounded online aggregation.
- `SF10_CustomObjective.mqh` applies hard gates and conservative scoring.
- `SF10_PassSummary.mqh` defines the compact cross-agent payload.
- `SF10_OptimizationFrames.mqh` owns `FrameAdd` and `FrameNext` integration.
- `SF10_SelectedPassCollector.mqh` retains a deterministic bounded top-N set.
- `SF10_DifferentialComparator.mqh` classifies virtual/tester divergence.
- `SF10_ResearchHarness.mqh` composes the complete phase.

## Operational consequences

The fast optimization loop writes no full event ledger per pass. It returns a custom criterion and sends a fixed-width summary. The controlling terminal collects summaries, selects passes, and emits rerun requests. A selected pass must be rerun with the required tester fidelity before its result can proceed to statistical validation.

## Acceptance questions

- Can the run be reproduced from its manifest and exact inputs?
- Does the same outcome stream generate the same metrics hash and objective?
- Are rejected passes visible with an explicit reason?
- Are late frames drained before final selection?
- Is selected-pass order deterministic?
- Does real-tick validation reconcile with virtual outcomes within declared tolerances?

## Related contracts

- [[04_RUN_MANIFEST]]
- [[06_RESEARCH_METRICS_ACCUMULATOR]]
- [[10_OPTIMIZATION_FRAMES]]
- [[15_FIDELITY_LADDER]]
- [[25_DIFFERENTIAL_VALIDATION]]
- [[41_TEST_MATRIX]]

