---
title: Temporal Graph Models
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- governed-challenger
---

# Purpose

Combine sequence and relational structure for intermarket and multi-context state estimation.

## Capability tier

**Governed Challenger**

## System design

### Temporal nodes

Node states update only when their source event is known.

### Relational memory

Edges carry age, confidence, source, and regime validity.

### Architectures

Temporal message passing and graph attention are challengers to explicit graph summary features.

### Policy boundary

Graph outputs are features or scores; graph topology cannot create new tradable contexts.

## Input contracts

- `TemporalGraphSnapshots`
- `NodeEventStreams`

## Output contracts

- `TemporalGraphEmbedding`
- `EdgeAttribution`
- `GraphDriftSignals`

## Measurement framework

- Dynamic-edge ablation.
- Missing-node robustness.
- Cross-market utility uplift.
- Topology drift.

## Adversarial questions

- Are edges estimated with future returns?
- Does graph attention concentrate on a leakage node?
- Can stale nodes influence decisions after expiry?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[Graph_Representation_Learning]]
