---
title: Distributional, Survival and Tail Learning
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- deep-design
- core-production
---

# Objective

Model event timing, censoring and full economic outcome distributions rather than binary win/loss or mean return.

## Capability tier

**Core Production**

# Non-negotiable principles

- Fill, stop, target, trail, invalidation, cancellation and expiry are competing events.
- Censoring preserves information.
- Tail/path metrics are primary for convex and trend profiles.

# Reference architecture

- Discrete/continuous survival heads model event hazards.
- Competing-risk heads estimate cause-specific and cumulative incidence.
- Distributional heads estimate quantiles, mixtures, expectiles or discrete distributions for net R, MFE, MAE, hold and giveback.
- Shared representation supports calibrated task-specific heads.

# Algorithms and decision logic

- Likelihood/IPCW handles right and interval censoring.
- Monotone parameterization controls quantile crossing.
- Tail calibration measures exceedance and expected shortfall.
- Profile targets include P(reach kR), smoothness, trail capture and capital-time.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `EventDefinitionRegistry` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `CensoringPolicy` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `SurvivalDataset` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `DistributionalModelCard` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `TailCalibrationReport` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `CompetingRiskPrediction` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Brier
- Time AUC
- Concordance
- Integrated calibration
- Quantile loss
- Tail exceedance
- Expected-shortfall error

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Only completed trades are used. |
| Failure | Bar close assumes event order. |
| Failure | Mean hides catastrophic bimodality. |
| Failure | kR estimates use tiny samples. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Distributions calibrate chronologically.
- [ ] Uncertainty/censoring enter utility.
- [ ] Tail claims survive cluster bootstrap and stress.

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
