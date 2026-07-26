---
title: Counterfactual Outcome Cube Engine
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

Generate consistent sibling-treatment outcomes for each occurrence across paths, economics, brokers, delays, capacities and management policies.

## Capability tier

**Core Production**

# Non-negotiable principles

- One occurrence is the unit of opportunity; siblings are not independent.
- Observed historical decisions do not define the candidate universe.
- Replay is simulator evidence unless causal assumptions justify stronger claims.

# Reference architecture

- Cube axes include occurrence, treatment, path resolution, economics, broker, delay, capacity and stress.
- State machines emit entry, fill, stop, target, trail, management, expiry, invalidation, costs, utility and censoring.
- Manifest binds raw lineage, simulator version, treatment universe, ambiguity policy and evidence class.

# Algorithms and decision logic

- Event-sourced replay evaluates all siblings against one ordered path.
- Path ambiguity produces bounds or conservative ordering.
- Censoring separates unresolved horizons from zero outcomes.
- Within-occurrence pair deltas and ranks reduce nuisance variation.
- Compression retains sufficient statistics plus full replay references.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `OutcomeCubePlan` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `OutcomeCell` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `PathAmbiguityRecord` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `CensoringRecord` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `SiblingDeltaTable` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `OutcomeCubeManifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Completion
- Ambiguity rate
- Treatment coverage
- Replay determinism
- Bound width
- Storage/compute per occurrence

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Only chosen treatments are labelled. |
| Failure | Non-fills are removed. |
| Failure | Censored outcomes become zero. |
| Failure | Candidates use inconsistent cost/path assumptions. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Siblings share occurrence/path identity.
- [ ] Cube rebuild is deterministic.
- [ ] Claims distinguish predictive, simulator-counterfactual and causal.

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
