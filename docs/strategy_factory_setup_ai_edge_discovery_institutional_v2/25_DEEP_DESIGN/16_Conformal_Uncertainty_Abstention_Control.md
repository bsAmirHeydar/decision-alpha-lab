---
title: Conformal Uncertainty, Selectivity and Abstention Control
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- deep-design
- core-production
---

# Objective

Turn uncertainty and support into explicit decision controls with calibrated prediction sets/risk bounds and measurable coverage-selectivity trade-offs.

## Capability tier

**Core Production**

# Non-negotiable principles

- Abstention protects alpha and capital.
- Aleatoric, epistemic, calibration, transport, execution and support uncertainty are separated.
- Conformal guarantees are assumption-bounded; dependent drifting data requires appropriate variants.

# Reference architecture

- Base predictors output probabilities, quantiles, ranks and uncertainty.
- Dedicated calibration layer uses classical calibration and conformal/risk-control methods.
- Selective policy accepts only when utility lower bound, support, calibration and capacity pass.
- Fallback routes to simpler model, manual, Skip or Reject.

# Algorithms and decision logic

- Blocked/rolling conformal preserves time/cluster assumptions.
- Risk control tunes thresholds for false-trade, tail or unsafe-selection losses.
- Ensembles estimate epistemic disagreement.
- Support combines density/distance, overlap, views, domain shift and novelty.
- Coverage-selectivity curves determine the operating point.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `CalibrationPlan` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `ConformalPolicy` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `UncertaintyDecomposition` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `SupportAudit` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `SelectivityCurve` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `FallbackDirective` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Calibration error
- Conditional coverage
- Risk exceedance
- Acceptance
- Utility/selectivity
- OOD detection
- Fallback correctness
- Decision instability

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | IID guarantee is claimed under dependence. |
| Failure | Uncertainty is one neural variance. |
| Failure | Threshold is tuned on final utility. |
| Failure | Abstention is disabled under pressure. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Operating point freezes before protected evaluation.
- [ ] Risk control is monitored under drift.
- [ ] Invalid/unsupported paths fail closed.

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
