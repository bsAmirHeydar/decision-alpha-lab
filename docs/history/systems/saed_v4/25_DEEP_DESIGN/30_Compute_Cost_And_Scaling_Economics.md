---
title: Compute Economics, Scaling Laws and Research Capital Discipline
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

Treat compute, data, storage, latency and human review as capital allocations and require advanced model scale to demonstrate economically meaningful marginal research value.

## Capability tier

**Core Production**

# Non-negotiable principles

- Bigger models are challengers until they earn protected incremental value.
- Compute cost includes energy, queue delay, storage, data preparation, validation and operational complexity.
- Scaling decisions are based on empirical curves and evidence bottlenecks, not prestige.
- Research programs have budget, stop-loss, salvage and reuse plans.
- Inference cost and runtime portability are part of model selection.

# Reference architecture

- Cost telemetry attributes resources to program, trial, model family, fold, artifact and evidence role.
- Scaling laboratory measures performance versus parameters, tokens/events, context length, resolution and compute.
- Budget allocator compares model scaling with additional data, replay fidelity, labels, nulls and validation.
- Inference economist estimates latency, memory, export, MQL5 feasibility and monitoring overhead.
- Carbon/energy and geographic constraints can be included where relevant.
- Research-finance dashboard reports cost per falsification, stable candidate, promotion and live utility.

# Algorithms and decision logic

- Fit empirical scaling curves with uncertainty and detect saturation or overfitting regions.
- Run controlled compute-matched comparisons between architectures.
- Estimate opportunity cost of one advanced run versus many baselines, data fixes or challenge tests.
- Use early stopping only where final-rank correlation has been certified.
- Apply budget stop-loss when evidence quality, support or economics cannot meet minimum gates.
- Include inference/export/parity cost in Pareto selection.
- Allocate a protected budget to reproducibility, red-team and prospective evidence.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `compute_budget` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `cost_telemetry` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `scaling_study` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `budget_decision` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `inference_cost_profile` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `research_finance_report` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Cost per accepted evidence claim.
- Protected utility uplift per unit compute.
- Scaling slope and saturation point.
- Training-to-inference total cost of ownership.
- Budget share for baselines, challenge and reproduction.
- Unused/stranded artifact and storage cost.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Massive search is used to compensate for poor context truth. |
| Failure | Only successful runs receive cost attribution. |
| Failure | Advanced model wins by using more data or folds than baseline. |
| Failure | Export and runtime costs appear after selection. |
| Failure | Budget pressure cuts independent validation first. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Compute-matched and evidence-matched comparisons exist.
- [ ] All trial statuses carry cost.
- [ ] Scaling beyond baseline has a predeclared economic thesis.
- [ ] Validation/reproduction budgets are protected.
- [ ] Runtime total cost is included in selection.

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
