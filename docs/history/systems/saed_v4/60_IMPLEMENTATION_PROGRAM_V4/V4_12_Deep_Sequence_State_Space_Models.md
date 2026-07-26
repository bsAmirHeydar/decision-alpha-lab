---
title: V4-12 Deep Sequence State Space Models
status: implemented-reference
version: 4.1.0
created: '2026-07-13'
updated: '2026-07-15'
capability_tier: governed-challenger
tags: [saed-v4, implementation, roadmap, implemented-reference]
---

# Phase V4-12: Deep Sequence and State-Space Models

## Implementation status

SAED V4-12 now has a complete deterministic synthetic-reference implementation. It consumes the exact frozen V4-11 tokenizer and encoder hashes, compiles causal root-context sequences, evaluates six architecture families, fits self-supervised next-representation readouts, proves streaming/chunk/restart parity, records state probes and ablations, registers conformant research checkpoints, creates a bounded distilled state and freezes the V4-13 handoff.

## Delivered architecture families

1. EMA recurrent baseline.
2. Causal convolution baseline.
3. Diagonal continuous-time state-space model.
4. Selective state-space model.
5. Local causal attention.
6. Hybrid selective-SSM and local-attention model.

## Closed evidence boundary

The implementation uses the synthetic V4-11 corpus only. Sequence cores are deterministic fixed reference parameterizations; only closed-form next-representation readouts are fitted. No outcome cube, execution twin, protected-final, prospective, shadow or live artifact is an input. No real alpha, treatment ranking, runtime parity or production authorization is claimed.

## Acceptance evidence

- Closed schemas and unknown-field rejection.
- Exact V4-11 hash binding.
- Known-time and future-suffix invariance.
- Batch/streaming, chunk and snapshot/restart parity.
- State collapse, stability and truncation controls.
- Baseline preservation and fixed-budget tournament.
- Canonical checkpoint registry, integrity receipt and independent replay.
- Python authority boundary, Obsidian and MQL5 static validation.

## Next phase

The next phase is [[V4_13_Graph_And_Hypergraph_Models|V4-13 Graph and Hypergraph Models]]. It may read the exact V4-12 registry, champion and distilled-state hashes to build reference graph challengers. It may not mutate V4-12 evidence or infer decision authority from synthetic-reference ranking.

## Detailed delivery

See [[README|SAED V4-12 Delivery Index]] under `62_PHASE_DELIVERIES_V4/V4_12`.
