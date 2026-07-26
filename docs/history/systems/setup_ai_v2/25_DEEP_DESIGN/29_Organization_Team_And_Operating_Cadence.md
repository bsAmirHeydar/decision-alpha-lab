---
title: Institutional Organization, Teams and Operating Cadence
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

Define the human operating model required to build, challenge, govern and run the system at institutional scale without collapsing research, validation, risk and release authority into one team.

## Capability tier

**Core Production**

# Non-negotiable principles

- Segregation of duties is an architecture requirement.
- Research velocity is increased through reusable platforms and clear decision rights, not weaker review.
- Owners are accountable for assumptions, artifacts, incidents and retirement—not only model performance.
- Committees review machine evidence and unresolved limitations, not presentation quality.
- Operating cadence includes routine falsification and retirement, not only new model launches.

# Reference architecture

- Context Science owns doctrine and occurrence semantics.
- Setup/AI Research owns hypotheses, treatments, models and experiment manifests.
- Data/Replay Engineering owns event truth, outcome cube and point-in-time correctness.
- Independent Validation owns statistical challenge, causal audit, model risk and promotion recommendation.
- Platform/MLOps owns compute, registries, reproducibility and artifact delivery.
- Risk/Portfolio owns capital limits, reservation and portfolio veto.
- Runtime/Execution owns compilation, parity, broker adapters and reconciliation.
- Operations/Release owns authorization, incident response, rollback and evidence retention.

# Algorithms and decision logic

- Run weekly research review focused on falsifiable progress and blocked assumptions.
- Run monthly model-risk review for open findings, drift, waivers and challenger status.
- Run quarterly portfolio/research review for edge decay, concentration, memory and resource allocation.
- Require pre-mortem before protected evidence and post-mortem after rejection, incident or retirement.
- Use RACI and signed decision records for every promotion, waiver, release and rollback.
- Measure team output through validated reusable evidence and avoided failure, not raw trial count.
- Maintain an on-call and incident command structure for runtime and data failures.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `team_charter` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `raci_matrix` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `review_packet` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `decision_record` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `waiver_record` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `incident_command_record` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `quarterly_operating_review` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Time from hypothesis to valid falsification.
- Independent validation backlog and review latency.
- Open findings/waivers by age and severity.
- Reuse of data, treatment, model and challenge assets.
- Incident response and rollback time.
- Retired or rejected candidates relative to promotions.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Researcher validates and promotes their own model. |
| Failure | Platform team changes semantics to meet delivery deadlines. |
| Failure | Committees approve opaque slide summaries without artifacts. |
| Failure | Waivers never expire. |
| Failure | Trial volume is rewarded more than evidence quality. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Research, validation, risk and release owners are distinct.
- [ ] Decision rights and escalation paths are documented.
- [ ] Review cadences consume signed artifact packets.
- [ ] Waivers and open findings have owners and expiry.
- [ ] Incident and retirement responsibilities are operational.

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
