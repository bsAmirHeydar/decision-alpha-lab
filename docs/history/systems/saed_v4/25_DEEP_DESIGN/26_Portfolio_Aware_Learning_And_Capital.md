---
title: Portfolio-Aware Learning, Capital Efficiency and Capacity
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- deep-design
- governed-challenger
---

# Objective

Evaluate setup candidates as marginal contributors to an existing portfolio rather than isolated trades, while preserving the separation between research utility, capital policy and hard portfolio authorization.

## Capability tier

**Governed Challenger**

# Non-negotiable principles

- Standalone edge is necessary but not sufficient for capital allocation.
- Portfolio-aware objectives may inform ranking but cannot bypass I17 reservations, limits or vetoes.
- Unknown dependence is penalized conservatively rather than treated as diversification.
- Capacity, turnover, liquidity and capital occupancy are economic labels, not post-hoc reporting fields.
- Capital scaling cannot manufacture evidence for a weak context-treatment relationship.

# Reference architecture

- Edge genome publishes return distribution, tail shape, horizon, exposures, context cluster, capacity and decay state.
- Dependence service estimates symbol, currency, session, anatomy, event and empirical dependence with fallback bounds.
- Marginal-utility simulator inserts candidate outcomes into frozen portfolio states across folds.
- Capital-policy laboratory evaluates fixed cash, fractional, volatility, drawdown-responsive and fractional-Kelly challengers.
- Capacity model maps requested size to fill, impact, slippage and utility degradation.
- Portfolio-aware selector emits a research score plus assumptions; I17 remains sole allocation authority.

# Algorithms and decision logic

- Compute standalone and marginal expected utility, expected shortfall, drawdown contribution and capital occupancy.
- Use clustered bootstrap and regime-conditioned dependence rather than a single full-sample correlation matrix.
- Apply robust covariance/dependence uncertainty sets and conservative fallback for sparse pairs.
- Estimate capacity curves from executable fill/impact models and stress them with liquidity haircuts.
- Run sequence Monte Carlo under capital policies including gaps, delayed de-risking and clustered losses.
- Compare ranking stability when current portfolio composition, dependence and capacity assumptions change.
- Freeze portfolio snapshot or simulation policy inside each experiment to avoid hindsight allocation.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `edge_genome` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `portfolio_state_snapshot` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `dependence_manifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `capacity_curve` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `capital_policy` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `marginal_value_report` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `portfolio_research_score` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Standalone versus marginal utility.
- Expected shortfall and drawdown contribution.
- Capital occupancy and time-underwater contribution.
- Capacity-adjusted utility and impact elasticity.
- Ranking stability across portfolio states and dependence stress.
- Concentration and shared-event exposure.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | A strong standalone strategy duplicates existing exposure. |
| Failure | Sparse dependence is estimated as zero. |
| Failure | Capital policy is optimized on the same locked outcomes as setup selection. |
| Failure | Capacity is inferred from bar volume without execution truth. |
| Failure | Portfolio-aware model learns future portfolio composition. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Standalone and marginal evidence are reported separately.
- [ ] Dependence uncertainty and conservative fallback are explicit.
- [ ] Capital policies have independent trials and evidence roles.
- [ ] I17 hard reservation and veto remain authoritative.
- [ ] Capacity and liquidity stress can force Skip or de-risk.

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
