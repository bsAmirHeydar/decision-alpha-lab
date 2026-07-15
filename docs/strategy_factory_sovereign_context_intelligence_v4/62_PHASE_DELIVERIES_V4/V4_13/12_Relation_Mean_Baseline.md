---
title: SAED V4-13 — Relation Mean Baseline
status: implemented-reference
version: 1.0.0
created: '2026-07-15'
updated: '2026-07-15'
tags: [saed-v4, v4-13, graph-learning, hypergraph-learning]
---
# SAED V4-13 — Relation Mean Baseline

A simple mean propagation baseline is preserved as the mandatory complexity comparator.

## Design detail

The implementation treats graph structure as governed evidence rather than an informal feature container. Nodes retain source hashes, semantic keys, event time, known time, quality and frozen lineage. Hyperedges retain relation kind, complete bounded membership, knowledge timestamp and source-edge hash. Pairwise projection is a derived model view, never a replacement for canonical hyperedge truth. Sequence-state enrichment is read-only and bound to the exact V4-12 distillation hash.


## Authority and evidence boundary

This phase is a deterministic synthetic-reference research capability. It reads exact frozen V4-05 semantic-temporal hypergraph evidence and exact frozen V4-12 sequence-state artifacts. It cannot mutate upstream truth, infer a new canonical relation, consume an Outcome Cube or Execution Digital Twin as supervision, rank or select a Treatment, allocate capital, activate an MT5 runtime generation, or submit an order. Every checkpoint is marked `production_eligible=false` and `runtime_authority=false`.

## Engineering invariant

Known-time is enforced before topology construction. A node or hyperedge whose knowledge timestamp exceeds the frozen cutoff is rejected rather than silently filtered into training. Node identity, edge identity, relation vocabulary, incidence membership, upstream hashes, graph compilation and checkpoint registration are canonicalized and hashed. Unknown fields in external contracts are rejected. Failure is fail-closed and produces no trading side effect.

## Evidence implemented

The local reference suite includes closed schemas, golden and negative fixtures, deterministic replay, topology mutation tests, future-suffix rejection, node-order invariance, contamination controls, fixed compute and exposure accounting, baseline preservation, model comparison, immutable checkpoint registration, an integrity Merkle receipt, an incident template and a hash-frozen handoff. Static MQL5 mirrors are included only for contract review; real MetaEditor compilation and terminal differential parity remain external evidence.

## Residual limitation

The graph corpus is synthetic and frozen. Model parameters are deterministic reference parameterizations and the evaluation tasks are outcome-free self-supervision. The results do not establish real alpha, causal treatment value, prospective performance, broker/runtime parity or production authorization.


## Navigation

[[00_Executive_Summary|Executive Summary]] · [[02_Authority_Matrix|Authority Matrix]] · [[25_Contamination_Firewall|Contamination Firewall]] · [[42_Acceptance_Criteria|Acceptance Criteria]] · [[50_V4_14_Handoff|V4-14 Handoff]]
