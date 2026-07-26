---
title: Self-Supervised Market Pretraining Curriculum
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- deep-design
- governed-challenger
---

# Objective

Learn transferable representations from unlabeled histories while preventing temporal leakage, identity memorization and protected-role contamination.

## Capability tier

**Governed Challenger**

# Non-negotiable principles

- Pretraining is a separate experiment with role, exposure, checkpoint and representation cards.
- Augmentations preserve market semantics and known time.
- Representations earn use only through downstream uplift and leakage probes.

# Reference architecture

- Curriculum covers local microstructure, multi-resolution structure, context transitions, intermarket relations, regime invariance and treatment-relevant probes.
- Objectives include masked patch reconstruction, denoising, causal forecasting, temporal contrast, cross-view prediction, order discrimination and lifecycle transition.
- Separate encoders serve price/volume, quote, context lifecycle, graph, calendar and execution views.

# Algorithms and decision logic

- Causal masks prevent attention beyond known time.
- Contrastive positives are semantic without future regime labels; negatives are hard but time-safe.
- View dropout teaches degradation and required-view logic.
- Probes measure future, symbol, timestamp, outcome and regime shortcuts.
- Checkpoint selection uses role-safe transfer tasks, not protected edge performance.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `PretrainingCorpusManifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `AugmentationPolicy` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `EncoderArchitecture` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `CheckpointLineage` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `RepresentationCard` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `ProbeSuiteReport` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Probe uplift
- Transfer efficiency
- Embedding stability
- Future leakage AUC
- Identity shortcut score
- View ablation
- Embedding drift

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Masking leaks future through normalization. |
| Failure | Embeddings memorize symbol outcomes. |
| Failure | Prospective data updates tokenizer. |
| Failure | Checkpoint selected on final edge results. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Pretraining can be removed without invalidating baseline.
- [ ] Representations improve multiple chronological downstream tasks.
- [ ] Leakage and shortcut probes remain within limits.

# Required evidence packet

- Specification and assumption cards.
- Code, environment, data and artifact hashes.
- Positive, negative, boundary, mutation and adversarial tests.
- Baseline, ablation, stress, transport and reproducibility reports.
- Open limitations, kill criteria, downstream handoff and rollback path.

# Related architecture

- [[00_Home]]
- [[UCEE_I01_I18_Compatibility]]
- [[Anti_Overfit_Master_Protocol]]
- [[Promotion_Dossier_And_Signed_Admission]]
- [[Release_And_Production_Qualification]]
