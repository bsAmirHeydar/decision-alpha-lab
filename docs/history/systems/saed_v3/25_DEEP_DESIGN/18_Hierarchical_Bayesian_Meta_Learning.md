---
title: Hierarchical Bayesian Meta-Learning and Cross-Context Priors
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

Create statistically disciplined transfer across context families, symbols, sessions and payoff profiles without allowing pooled averages to erase local evidence or cause negative transfer.

## Capability tier

**Governed Challenger**

# Non-negotiable principles

- Every transfer relationship is explicit, versioned and challengeable; similarity is never inferred solely from labels.
- Partial pooling is preferred to global pooling or isolated estimation when the exchangeability assumptions survive falsification.
- Posterior uncertainty, prior sensitivity and conflict diagnostics are first-class promotion evidence.
- No prior may override hard context support, known-time, treatment compatibility, cost feasibility or UCEE authority boundaries.
- Weak contexts may borrow strength only from evidence partitions declared before locked evaluation.

# Reference architecture

- Context-family hierarchy: global → anatomy family → context version → symbol/feed → regime/session → payoff profile → entry mechanism.
- Prior registry stores provenance, effective sample size, half-life, transport scope and revocation criteria.
- Meta-feature encoder estimates structural similarity using only training-role evidence and frozen ontology descriptors.
- Hierarchical generalized linear, survival and distributional heads provide transparent production baselines.
- Neural meta-learners and amortized posterior networks remain challengers behind posterior predictive checks.
- Conflict monitor compares local likelihood with imported prior and can force no-pooling or quarantine.

# Algorithms and decision logic

- Fit non-centered hierarchical models with context-specific intercepts/slopes and global shrinkage priors.
- Use leave-one-context-out posterior predictive checks before enabling cross-context borrowing.
- Estimate transfer value as paired incremental utility relative to local-only and pooled baselines.
- Apply robust or mixture priors when context families exhibit outlier behavior.
- Use prior-data conflict statistics, posterior contraction, calibration and coverage to bound borrowing.
- Run negative-transfer stress by permuting family assignments and inserting deliberately incompatible donor contexts.
- Freeze the donor set, hierarchy, prior family and hyperprior search budget inside every experiment manifest.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `meta_learning_program` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `prior_registry` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `context_similarity_manifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `posterior_artifact` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `transfer_audit` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `negative_transfer_report` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Leave-one-context-out utility uplift versus local-only baseline.
- Posterior predictive coverage and calibration by context.
- Prior effective sample size and local-to-prior information ratio.
- Negative-transfer rate and worst subgroup degradation.
- Sensitivity to prior family, scale and donor-set perturbation.
- Decision agreement and abstention change induced by transfer.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | False exchangeability creates confident but wrong transfer. |
| Failure | Large donor contexts dominate economically distinct recipients. |
| Failure | Similarity encoder leaks locked outcomes into donor selection. |
| Failure | Hyperprior search becomes an uncounted trial universe. |
| Failure | Posterior means hide multimodality or regime conflict. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Donor/recipient graph and exchangeability assumptions are predeclared.
- [ ] Local-only, pooled and hierarchical baselines share identical folds and economics.
- [ ] No recipient suffers unbounded downside under negative-transfer stress.
- [ ] Prior sensitivity and leave-one-context-out challenge pass.
- [ ] Transferred model can fall back to local/manual/skip without state mismatch.

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
