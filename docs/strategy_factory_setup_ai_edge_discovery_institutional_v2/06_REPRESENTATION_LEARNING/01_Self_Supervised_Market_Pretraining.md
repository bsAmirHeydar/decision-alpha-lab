---
title: Self-Supervised Market Pretraining
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- governed-challenger
---

# Purpose

Learn reusable market-state representations from unlabeled multi-market histories without allowing pretraining to contaminate locked evaluation roles.

## Capability tier

**Governed Challenger**

## System design

### Pretext families

Masked segment reconstruction, forecasting, contrastive temporal alignment, cross-view prediction, denoising, order-aware objectives, and regime discrimination.

### Role firewall

Pretraining data is declared by time and market; no final-test or prospective data can influence tokenizer, normalization, architecture choice, or checkpoints.

### Multi-resolution views

Tick/quote, bar, context lifecycle, intermarket graph, and session/calendar streams are encoded separately before controlled fusion.

### Representation audit

Linear probes, nearest-neighbor inspection, invariance tests, and leakage probes determine what information the embedding contains.

## Input contracts

- `PretrainingCorpusManifest`
- `ViewSchemas`
- `AugmentationPolicy`

## Output contracts

- `EncoderCheckpoint`
- `RepresentationCard`
- `ProbeReport`

## Measurement framework

- Transfer uplift over raw-feature baselines.
- Representation stability across seeds and periods.
- Probe leakage and shortcut scores.
- Embedding drift.

## Adversarial questions

- Does masking permit future context?
- Does contrastive sampling encode symbol identity instead of state?
- Did architecture selection inspect locked roles?

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

- [[Time_Series_Foundation_Model_Adapters]]
