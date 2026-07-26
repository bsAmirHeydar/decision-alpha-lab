---
title: Causal Treatment-Effect Learning Stack
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- deep-design
- governed-challenger
---

# Objective

Estimate heterogeneous incremental value of treatment choices under explicit identification, overlap and sensitivity controls.

## Capability tier

**Governed Challenger**

# Non-negotiable principles

- Prediction, replay counterfactuals and causal effects are distinct.
- Every causal claim has assumption and overlap cards.
- Doubly robust, orthogonal and honest estimators precede neural causal models.

# Reference architecture

- Identification routes include randomized variation, natural experiments, explicit propensities, simulator assumptions and observational unconfoundedness.
- Cross-fitted nuisance models estimate propensity and outcomes.
- Effect learners include DR/R/X/T, causal forests, orthogonal forests and neural challengers.
- Policy learner maps effects to finite treatments with support masks.

# Algorithms and decision logic

- Cluster cross-fitting keeps sibling treatments together.
- Overlap trimming/partial identification replaces extrapolation.
- Sensitivity varies hidden confounding, simulator error, policy selection and propensity misspecification.
- Conformal effect intervals abstain when lower bound does not beat Skip.
- Transport targets explicit symbol/broker/regime populations.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `CausalAssumptionCard` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `PropensityModelCard` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `OverlapReport` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `EffectModelCard` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `SensitivityReport` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `CausalPolicyValueReport` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Overlap
- Balance
- DR value
- Interval coverage
- Sensitivity threshold
- Transport error
- Causal/predictive rank agreement

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Replay cube is called causal. |
| Failure | Human discretion has unrecorded confounding. |
| Failure | Rare treatments get positive extrapolation. |
| Failure | Propensity model sees protected outcomes. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Causal/predictive evidence reported separately.
- [ ] Low overlap abstains.
- [ ] Value is robust across nuisance models and sensitivity.

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
