---
title: Cross-Context Meta-Learning
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- governed-challenger
---

# Purpose

Transfer reusable representations and priors across context families while protecting local semantics, support, and evaluation independence.

## Capability tier

**Governed Challenger**

## System design

### Transfer units

Feature encoders, treatment embeddings, payoff priors, fill models, trail representations, and uncertainty priors.

### Meta-training

Context programs are tasks; leave-one-context, leave-one-market, and chronological meta-validation test transfer.

### Adapters

Local heads or low-rank adapters retain context-specific calibration.

### Negative transfer

Transfer is rejected when local simple models or from-scratch models perform more robustly.

## Input contracts

- `ContextPrograms`
- `SharedRepresentations`
- `TaskSplits`

## Output contracts

- `MetaModel`
- `ContextAdapters`
- `TransferDossier`

## Measurement framework

- Few-shot uplift.
- Negative-transfer rate.
- Leave-context-out performance.
- Calibration transfer.

## Adversarial questions

- Does meta-training include target-context future data?
- Do dominant contexts overwhelm rare ones?
- Is semantic incompatibility hidden by embeddings?

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

- [[Hierarchical_Bayesian_Edge_Priors]]
