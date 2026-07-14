---
title: Conservative Offline Policy Learning
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- deep-design
- research-only
---

# Objective

Explore sequential entry, management, trail and exit policies from static trajectories while suppressing unsupported actions and requiring trustworthy OPE.

## Capability tier

**Research-Only**

# Non-negotiable principles

- Offline RL is used only where sequential decisions add measurable value.
- Action masks come from finite treatment state machines and hard risk.
- Policy value requires multiple OPE methods, replay and prospective challenge.

# Reference architecture

- Behavior model estimates historical/manual support.
- CQL lowers unsupported values; IQL avoids explicit unseen-action maximization; sequence challengers model trajectories.
- Safe projection maps proposals to valid supported actions or Abstain.
- Extraction produces an auditable graph or distilled bounded model.

# Algorithms and decision logic

- FQE, importance sampling, doubly robust OPE and replay must agree directionally.
- Uncertainty and behavior-closeness penalties rise in low-support states.
- Reward separates P&L, cost, tail, drawdown, time, turnover and violations.
- Stress perturbs costs, delays, state, reward weights and propensities.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `OfflineTrajectoryManifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `BehaviorPolicyCard` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `RewardContract` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `ActionMask` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `OPEReport` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `SafePolicyArtifact` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Conservative OPE
- Estimator disagreement
- OOD action rate
- Behavior divergence
- Q calibration
- Seed stability
- Prospective agreement

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Reward hacking exploits simulator. |
| Failure | Policy chooses absent actions. |
| Failure | OPE weights collapse ESS. |
| Failure | Returns-to-go leak future. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Sequential policy beats fixed baselines after penalties.
- [ ] Unsupported output projects to Abstain/Manual.
- [ ] Production requires distillation and UCEE gates.

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
