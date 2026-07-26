---
title: Failure Modes, Kill Criteria, Quarantine and Recovery
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

Predefine when research, models, policies, data assets, runtime generations and live authorizations must stop, quarantine, roll back, requalify or retire.

## Capability tier

**Core Production**

# Non-negotiable principles

- Kill criteria are written before the failure occurs.
- Fail-closed behavior protects capital and evidence integrity.
- Quarantine preserves artifacts and forensic state; it is not deletion.
- Recovery requires reconciliation and renewed qualification, not merely process restart.
- No commercial urgency can override critical data, risk, authorization or integrity failures.

# Reference architecture

- Failure taxonomy spans data, context, labels, models, causal assumptions, agents, compute, artifacts, runtime, broker, portfolio and operations.
- Health state machine supports healthy, watch, reduced, paused, quarantined, revoked and retired.
- Kill matrix maps condition severity to automatic and human actions.
- Incident ledger binds timeline, evidence, impacted artifacts, decisions and accounts.
- Recovery controller restores last admitted generation and reconciles decisions, reservations, orders and positions.
- Requalification path is scoped to affected assumptions and dependencies but cannot skip mandatory gates.

# Algorithms and decision logic

- Detect integrity mismatches, stale views, abnormal missingness, calibration drift, OOD, latency, reservation mismatch and authorization expiry.
- Use dual thresholds for early de-risk and hard kill where appropriate.
- Propagate dependency impact from a compromised artifact through the lineage graph.
- Freeze relevant logs, checkpoints and market/broker evidence on incident declaration.
- Reconcile expected versus actual state before resume.
- Run controlled recovery drills for disconnect, disk full, corrupt artifact, partial fill, clock shift and rollback.
- Retire candidates whose edge, capacity or assumptions no longer justify monitoring cost.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `failure_taxonomy` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `kill_matrix` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `health_state` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `incident_record` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `quarantine_record` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `recovery_checkpoint` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `requalification_plan` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `retirement_record` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Detection-to-kill and kill-to-safe-state latency.
- Incident completeness and forensic preservation.
- Rollback/reconciliation success.
- Recurring failure and ineffective remediation rate.
- Open quarantine duration and owner.
- False-positive kill versus missed critical failure.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | System continues because monitoring itself is degraded. |
| Failure | Restart is treated as recovery without reconciliation. |
| Failure | Quarantine artifacts are modified during investigation. |
| Failure | Authorization expiry fails to disable live action. |
| Failure | Retired edge is silently reintroduced through transfer learning. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Critical conditions trigger automatic fail-closed action.
- [ ] Recovery drills pass on clean and partial-state scenarios.
- [ ] Dependency impact and affected generations are traceable.
- [ ] Resume requires signed reconciliation and qualification.
- [ ] Retirement propagates to priors, memory and allowlists.

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
