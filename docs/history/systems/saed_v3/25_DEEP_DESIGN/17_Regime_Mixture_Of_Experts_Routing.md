---
title: Regime Specialists and Sparse Mixture-of-Experts Routing
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

Allow model specialization by regime while preventing hindsight labels, expert collapse and unstable routing.

## Capability tier

**Governed Challenger**

# Non-negotiable principles

- Regime is a known-time state estimate.
- Experts share action lattice and policy constraints.
- Routing uncertainty and fallback are explicit.

# Reference architecture

- Regime features include volatility, liquidity, trend/chop, correlation, session, event density, context mix and execution.
- Router may be rule, probabilistic, hidden-state, change-point or sparse gate.
- Experts differ in model, payoff support, objective or calibration while sharing evidence protocols.

# Algorithms and decision logic

- Load balancing and entropy regularization prevent collapse.
- Temporal smoothing limits route flapping.
- Competence calibrates on out-of-fold routed data.
- Unknown regimes route generalist/manual/abstain.
- Leave-one-regime-out tests transport.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `RegimeDefinition` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `RouterCard` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `ExpertRegistry` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `RoutingDecision` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `RoutingCalibrationReport` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `UnknownRegimeFallback` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Router calibration
- Expert utilization
- Expert uplift
- Route stability
- Unknown rate
- Generalist comparison
- Transport

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Regimes use full-period outcomes. |
| Failure | Future trend label routes expert. |
| Failure | Tiny experts overfit. |
| Failure | Routing changes after final results. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Regime reconstructs at known time.
- [ ] Experts beat generalist after penalties.
- [ ] Unknown routes abstain/fallback.

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
