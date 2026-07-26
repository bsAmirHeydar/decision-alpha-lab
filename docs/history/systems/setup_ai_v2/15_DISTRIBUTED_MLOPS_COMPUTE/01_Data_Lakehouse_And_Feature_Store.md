---
title: Data Lakehouse and Feature Store
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Provide versioned raw, curated, feature, embedding, outcome, and evidence layers without allowing online convenience to override research truth.

## Capability tier

**Core Production**

## System design

### Zones

Raw immutable events, validated canonical events, known-time features, treatment outcomes, datasets, and evidence marts.

### Feature definitions

Code, schema, timing, dependencies, freshness, offline/online parity, owner, and deprecation.

### Embedding store

Encoder version, input view hashes, precision, normalization, and support index.

### Access

Role- and purpose-based policies protect locked and prospective data.

## Input contracts

- `RawEvents`
- `FeatureDefinitions`
- `AccessPolicy`

## Output contracts

- `FeatureSnapshots`
- `EmbeddingArtifacts`
- `DataQualityMetrics`

## Measurement framework

- Offline/online parity.
- Freshness.
- Lineage completeness.
- Access violations.
- Storage cost.

## Adversarial questions

- Can a mutable feature overwrite history?
- Does online materialization use different joins?
- Are embeddings reused across incompatible encoders?

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

- [[Artifact_Graph_And_Content_Addressing]]
