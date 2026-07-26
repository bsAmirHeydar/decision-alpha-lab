---
title: End-to-End Institutional Reference Architecture
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

Specify the complete post-context operating system from immutable UCEE occurrence to governed treatment policy and production evidence.

## Capability tier

**Core Production**

# Non-negotiable principles

- Context semantics are upstream and immutable; SAED cannot rewrite context history.
- Research, selection, promotion, runtime, portfolio, execution and monitoring are separate authority domains.
- Every boundary exchanges typed versioned hash-bound artifacts.

# Reference architecture

- Ingress: UCEE context occurrence, views, feature DAG output, lineage, freshness and lifecycle.
- Treatment factory: archetypes, payoff profiles, entry mechanisms, trigger philosophies, stop/exit/management atoms, compatibility and dominance pruning.
- Truth factory: event replay, bid/ask path, fill hazard, adverse selection, costs, capacity, impact and outcome cube.
- Learning stack: manual/naive, supervised, ranking, survival, distributional, representation, causal, graph, world-model and research-only policy learning.
- Evidence stack: nested purged walk-forward, complete trial ledger, multiplicity, nulls, transport, stress, prospective challenge and model risk.
- Policy and production: I12 admission, I13 graph/fallback, I14 immutable runtime, I17 portfolio and I18 qualification.

# Algorithms and decision logic

- Candidate identity hashes occurrence, archetype, treatment atoms, economics and compiler version.
- Cluster identity binds all sibling treatments and Skip for one occurrence.
- Decision value combines net utility, tail, uncertainty, capacity and portfolio marginal-risk costs.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `ContextExploitationProgram` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `TreatmentUniverseManifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `OutcomeCubeManifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `TrainerProgram` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `PromotionDossier` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `RuntimeHandoff` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `MonitoringAssumptionContract` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Lineage completeness
- Replay agreement
- Feature parity
- Python/export/MQL5 parity
- Reservation reconciliation
- Decision latency

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Downstream recomputes or normalizes context evidence. |
| Failure | Model bypasses treatment lattice. |
| Failure | Partial bundle activates. |
| Failure | Portfolio or risk veto becomes a soft score. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] A golden occurrence replays raw event to final decision byte-for-byte.
- [ ] Removing any required artifact prevents activation.
- [ ] Python, export and MQL5 decisions agree within declared tolerance.

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
