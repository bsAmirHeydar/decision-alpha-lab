---
title: Data Contract and Bitemporal Market Truth
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

Make timing, revisions, feeds, symbols and derived observations auditable and immune to future leakage.

## Capability tier

**Core Production**

# Non-negotiable principles

- Every record has event time, known time, ingestion time, source time and revision identity.
- Historical correction never overwrites what was available to the original decision.
- Feed, broker, timezone, DST, symbol mapping, corporate action and session assumptions are artifacts.

# Reference architecture

- Raw append-only log stores quotes, trades, bars, depth, broker metadata, calendar and symbol-specification events.
- Canonicalization creates stable identities while retaining raw payload and source checksum.
- Bitemporal snapshots answer both what happened and what was known when.
- Data-quality state machine classifies complete, delayed, stale, revised, conflicted, missing, corrupt or unsupported.

# Algorithms and decision logic

- As-of joins require known_time <= decision_known_time and prohibit nearest-future joins.
- Future-suffix perturbation proves later data cannot change historical features or decisions.
- Revision replay compares original-knowledge and revised-truth outcomes without contaminating roles.
- Cross-feed reconciliation propagates timing, price, spread, high/low and session disagreement to robustness tests.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `RawEventEnvelope` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `CanonicalMarketEvent` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `BitemporalSnapshot` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `DataQualityEvent` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `FeedReconciliationReport` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `KnownTimeCertificate` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Late-event rate
- Revision rate
- Staleness
- Cross-feed disagreement
- As-of violations
- Future-suffix mutations
- Missingness by context/regime

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Bars are timestamped at close but treated available at open. |
| Failure | Corrected files replace decision-time files. |
| Failure | Timezone is inferred from machine locale. |
| Failure | Symbol changes are applied retroactively. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Features have machine-verifiable availability rules.
- [ ] Decisions reconstruct using only decision-time knowledge.
- [ ] Feed substitution and clock shifts are stress dimensions.

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
