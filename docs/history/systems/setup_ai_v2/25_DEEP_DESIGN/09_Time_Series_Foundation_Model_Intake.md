---
title: Time-Series Foundation Model Intake and Adaptation
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

Evaluate pretrained time-series models as representation or forecasting challengers without granting domain truth, causal authority or direct policy control.

## Capability tier

**Governed Challenger**

# Non-negotiable principles

- Foundation models are baselines/challengers, not automatic winners.
- Weights, license, training disclosure, architecture, context length, precision and code provenance are supply-chain artifacts.
- Zero-shot forecast accuracy is not trading utility.

# Reference architecture

- Adapter modes include frozen embedding, zero-shot forecast features, parameter-efficient tuning, supervised fine-tuning, distillation and ensemble features.
- Benchmark compares TimesFM/Chronos/MOMENT/Moirai-style families against seasonal naive, statistical, boosted, patch-transformer and SSM baselines.
- Financial adaptation uses covariate discipline, rolling evaluation, support diagnostics and domain-shift cards.

# Algorithms and decision logic

- Forecast distributions become decision features only through known-time-safe calibrated adapters.
- Fine-tuning occurs inside folds; checkpoints never see calibration or final roles.
- Distillation requires teacher/student disagreement and failure-set preservation.
- Foundation output never becomes action/treatment value without an economic learner.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `FoundationModelIntake` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `WeightProvenance` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `LicenseAndSBOM` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `AdapterConfig` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `DomainShiftCard` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `FoundationBenchmarkReport` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Zero-shot/adapted skill
- Economic uplift
- Calibration
- Latency/memory
- Transport
- Fine-tuning stability
- Complexity-adjusted value

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Benchmark contamination is ignored. |
| Failure | Training corpus may include evaluation periods. |
| Failure | Model is promoted because it is recent or large. |
| Failure | Remote inference creates opaque production dependency. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Economic—not merely predictive—uplift beats simple baselines.
- [ ] Supply-chain and provenance risks are documented.
- [ ] Deterministic local export or bounded fallback exists before production.

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
