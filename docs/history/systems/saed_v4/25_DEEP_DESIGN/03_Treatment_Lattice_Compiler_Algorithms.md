---
title: Finite Treatment Lattice Compiler — Algorithms and Invariants
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

Compile a bounded runtime-feasible action universe from context-compatible setup and execution atoms without combinatorial or post-test mutation.

## Capability tier

**Core Production**

# Non-negotiable principles

- Skip and Abstain are mandatory actions.
- Candidates are finite, versioned, deterministic and frozen before protected evaluation.
- Compatibility is semantic and economic, not merely syntactic.

# Reference architecture

- Registries cover archetypes, payoff, entry, trigger, stop, exit, trail, management, risk eligibility and expiry.
- Compiler passes validate schema, context eligibility, compatibility, broker feasibility, economics, state machine, dominance and identity.
- Pruning ledger preserves each removed candidate and reason.

# Algorithms and decision logic

- Constraint satisfaction removes incompatible combinations such as path-dependent trails without qualified path truth.
- Weak dominance pruning removes a candidate only when another is no worse across price, risk, target, cost, capacity and complexity.
- Symmetry control prevents mirrored or numerically equivalent candidates inflating multiplicity.
- Hierarchical expansion opens stop/exit/trail dimensions only after lower-complexity families survive.
- Candidate hash binds all atom versions, context support, broker and objective profile.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `TreatmentAtomRegistry` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `CompatibilityGraph` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `CompilerPlan` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `TreatmentCandidate` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `PruningLedger` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `TreatmentUniverseManifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Raw/retained count
- Dominance compression
- Invalid combination rate
- Search-space entropy
- Runtime feasibility
- Identity collisions

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Model invents arbitrary stop/target outside registry. |
| Failure | Parameters are added after final results. |
| Failure | Equivalent candidates count as independent trials. |
| Failure | Broker constraints are deferred to production. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Identical compiles are byte-identical.
- [ ] Every candidate has complete economic/state-machine semantics.
- [ ] Frozen universe changes require a new experiment and exposure entry.

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
