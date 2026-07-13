---
title: Experiment Search, Multi-Fidelity Optimization and Compute Allocation
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

Allocate finite research capital across hypotheses, model families, treatment candidates and evidence gaps while preserving complete trial accounting and preventing search from becoming an invisible source of overfit.

## Capability tier

**Core Production**

# Non-negotiable principles

- Compute is a governed research budget, not an entitlement.
- Every attempted configuration belongs to the multiplicity universe even when it fails, times out or is pruned.
- Multi-fidelity shortcuts may save cost but cannot substitute for final evidence roles.
- Search objectives are multi-objective and constraint-aware; no single scalar may hide tail, capacity or instability.
- Resource allocation must prefer information gain and falsification value over cosmetic leaderboard improvement.

# Reference architecture

- Program allocator assigns budgets across context families using evidence gap, expected value, novelty and reuse potential.
- Search controller executes frozen candidate generators, Bayesian optimization, successive halving and Pareto search.
- Fidelity ladder spans sample fraction, history length, fold count, model width, treatment resolution and path-replay precision.
- Trial ledger captures parent program, exact configuration, seed, environment, costs, status, artifacts and exposure events.
- Queue scheduler enforces GPU/CPU/memory/storage quotas, preemption rules and deterministic retry semantics.
- Compute economist records cost per falsified hypothesis, per stable candidate and per promoted basis point of utility.

# Algorithms and decision logic

- Use asynchronous successive halving only on training/inner-validation evidence and never on locked final or prospective data.
- Optimize Pareto fronts for utility, tail risk, stability, calibration, turnover, capacity, complexity and compute cost.
- Apply common random numbers and paired folds when comparing candidates to reduce comparison variance.
- Reserve explicit exploration budget for nulls, simple baselines, ablations and red-team challenges.
- Use value-of-information estimates to rank new experiments after accounting for correlation with existing trials.
- Block repeated searches on already-exposed locked evidence unless a new version and governance waiver are issued.
- Persist scheduler decisions so a recreated run yields the same candidate order under the same manifest.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `compute_budget` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `search_space_manifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `fidelity_schedule` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `trial_ledger` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `pareto_frontier` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `scheduler_decision_log` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `compute_cost_report` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- GPU/CPU hours and storage per program, candidate and accepted result.
- Fraction of budget spent on baselines, falsification and advanced models.
- Search-to-final rank correlation across fidelity levels.
- Pareto hypervolume on protected validation.
- Trial reproducibility and retry determinism.
- Compute cost per stable incremental utility unit.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Pruning favors noisy early winners and kills slow-learning robust models. |
| Failure | Locked data is queried repeatedly through search dashboards. |
| Failure | Failed trials disappear from multiplicity accounting. |
| Failure | Scheduler nondeterminism changes selection outcomes. |
| Failure | Compute scale substitutes for hypothesis quality. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Budget, search space, fidelity ladder and stopping rules are frozen.
- [ ] All attempted trials appear in the ledger.
- [ ] Finalists are retrained and evaluated from clean manifests.
- [ ] Compute and evidence roles are separated by access controls.
- [ ] Pareto selection includes stability, tail and capacity constraints.

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
