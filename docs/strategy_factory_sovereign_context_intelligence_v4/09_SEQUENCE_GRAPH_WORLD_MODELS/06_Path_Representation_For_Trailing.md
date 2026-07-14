---
title: Path Representation for Trailing
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- governed-challenger
---

# Purpose

Encode path shape, trend smoothness, pullback geometry, and state transitions for P3 and P4 trailing styles.

## Capability tier

**Governed Challenger**

## System design

### Path descriptors

Excursion curves, drawup/drawdown, swing graph, realized volatility, directional persistence, and local roughness.

### Learned encoders

Causal sequence embeddings are challengers to explicit descriptors.

### Counterfactual trails

Multiple trail state machines are replayed on identical paths.

### Outcome attribution

Separate entry quality, path quality, trail quality, and exit timing.

## Input contracts

- `PathEvents`
- `TrailCandidates`
- `ContextFeatures`

## Output contracts

- `PathEmbedding`
- `TrailSuitability`
- `TrailAttribution`

## Measurement framework

- Tail capture ratio.
- Giveback.
- Premature exit.
- Path-cluster stability.
- Trail uplift.

## Adversarial questions

- Does the path representation use post-exit future continuation?
- Is trail tuning tied to a few smooth trends?
- Are intrabar ambiguities resolved optimistically?

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

- [[Exit_Trail_Management_Library]]
