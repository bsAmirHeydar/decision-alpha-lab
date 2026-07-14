---
title: Multi-Objective Utility and Pareto Governance
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- deep-design
- core-production
---

# Objective

Prevent a single metric such as win rate, Sharpe or mean R from defining edge and encode profile objectives inside a common institutional utility framework.

## Capability tier

**Core Production**

# Non-negotiable principles

- Each payoff profile has its own primary objective and hard constraints.
- Cross-profile comparison occurs after costs, tail, uncertainty, capacity, capital time and portfolio effects.
- Safety and evidence constraints are non-compensatory.

# Reference architecture

- Objective profiles separate prediction loss, decision utility, evidence, operations and portfolio value.
- Pareto frontier retains candidates trading hit rate, convexity, tail capture, drawdown, turnover, latency, capacity and complexity.
- Lower-confidence-bound utility combines point estimates with epistemic, calibration, transport and execution uncertainty.

# Algorithms and decision logic

- P1/P5 maximize calibrated hit probability subject to net reward >=1R and tail/cost constraints.
- P2 optimizes right-tail utility and winner-removal robustness.
- P3 optimizes trail capture, giveback and path stability.
- P4 optimizes trend capture per risk-capital time with regime and underwater constraints.
- Portfolio utility subtracts concentration, dependence, turnover, impact and capacity scarcity.
- Robust utility evaluates declared stress sets, not one base case.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `ObjectiveProfile` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `ConstraintSet` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `UtilityDecomposition` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `ParetoFrontier` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `RobustUtilityReport` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `PortfolioValueAttribution` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Net utility
- Expected shortfall
- Utility lower bound
- Tail capture
- Hit calibration
- Capital-time return
- Capacity utility
- Pareto stability
- Complexity-adjusted uplift

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | High win rate hides catastrophic tails. |
| Failure | Convex system is rejected for low win rate. |
| Failure | Trail maximizes in-sample MFE. |
| Failure | Non-fill opportunity cost is ignored. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Leaderboards show objective and constraint decomposition.
- [ ] No candidate wins by violating a hard constraint.
- [ ] Ranking remains stable across plausible weights and stresses.

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
