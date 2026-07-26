---
title: Research Memory, Active Learning and Institutional Compounding
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

Convert every hypothesis, trial, failure, challenge, incident and live observation into a queryable memory graph that improves future experiment selection without contaminating protected evidence.

## Capability tier

**Core Production**

# Non-negotiable principles

- Negative evidence and abandoned paths are first-class assets.
- Memory entries are immutable claims linked to evidence, not free-form conclusions.
- Retrieval respects evidence role, exposure, entitlement and temporal validity.
- Active learning proposes experiments; it does not promote models or rewrite doctrine.
- Institutional learning is measured by avoided redundant work and better-calibrated priors.

# Reference architecture

- Knowledge graph links context, setup, treatment, feature, model, trial, evidence, failure, incident and runtime generation.
- Claim store records subject, predicate, object, uncertainty, scope, evidence class, owner and invalidation criteria.
- Embedding index supports semantic retrieval but never replaces canonical graph identity.
- Failure signature service clusters leakage, brittleness, cost, transport, execution and governance failures.
- Active experiment planner ranks proposals by expected information gain, economic value, reuse and cost.
- Exposure-aware retrieval blocks prospective/locked information from exploratory agents and training workflows.
- Memory compaction creates summaries while preserving source claims and dissent.

# Algorithms and decision logic

- Deduplicate hypotheses using ontology identity plus semantic similarity and treatment-lattice overlap.
- Estimate value of information from posterior uncertainty, decision sensitivity and downstream reuse.
- Use contextual bandit-style planning only for research allocation, with complete action/reward logging.
- Apply decay and validity windows to market-dependent claims while retaining historical truth.
- Retrieve nearest failures before launching a new experiment and require an explicit differentiation argument.
- Generate diagnostic packets from machine evidence, not narrative inference alone.
- Evaluate memory quality with held-out retrieval tasks and avoided-duplicate audits.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `research_claim` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `evidence_claim` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `failure_signature` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `memory_edge` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `experiment_proposal` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `retrieval_audit` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `diagnostic_packet` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Duplicate experiment avoidance.
- Failure reuse and preemption rate.
- Retrieval precision/recall for known evidence.
- Proposal information gain versus realized learning.
- Protected-evidence access violations.
- Time from incident or failure to reusable memory entry.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Narrative summaries become uncited institutional folklore. |
| Failure | Embedding retrieval leaks protected outcomes. |
| Failure | Active planner exploits noisy reward signals by proposing trivial experiments. |
| Failure | Old market claims remain treated as current. |
| Failure | Dissenting or failed evidence is compacted away. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Every claim links to evidence and invalidation criteria.
- [ ] Role-aware retrieval is tested.
- [ ] Negative evidence appears in proposal review.
- [ ] Active planner cannot execute or promote experiments autonomously.
- [ ] Memory summaries preserve source, uncertainty and dissent.

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
