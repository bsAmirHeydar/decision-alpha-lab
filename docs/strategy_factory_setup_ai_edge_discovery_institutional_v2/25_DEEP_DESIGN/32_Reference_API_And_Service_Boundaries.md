---
title: Reference APIs, Events and Service Boundaries
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

Define stable typed boundaries between context, treatment, replay, data, training, evidence, policy, portfolio, runtime and operations so the platform can scale organizationally without semantic drift.

## Capability tier

**Core Production**

# Non-negotiable principles

- Services exchange immutable versioned artifacts and events, not shared mutable database rows.
- APIs express semantics, known-time, support, evidence class and failure modes.
- Research and production planes are separated even when they share schemas.
- Idempotency and content identity are mandatory for long-running distributed workflows.
- Backward compatibility is explicit and bounded; silent coercion is forbidden.

# Reference architecture

- Context Registry API resolves exact context package and occurrence contracts.
- Treatment Compiler API produces finite candidates from approved registries and compatibility graphs.
- Replay/Outcome API simulates candidate paths and returns content-addressed outcome cubes.
- Dataset/Fold API materializes clustered point-in-time rows and protected roles.
- Trainer API consumes immutable manifests and emits predictions, metrics and model artifacts.
- Evidence API records trials, exposures, challenges, claims and promotion dossiers.
- Policy/Runtime API compiles admitted artifacts; Portfolio API reserves risk; Operations API authorizes release and recovery.
- Event bus publishes lifecycle events with schema registry and replayable offsets.

# Algorithms and decision logic

- Derive idempotency keys from semantic content plus caller scope.
- Use explicit request/response schemas with closed fields and version negotiation.
- Publish domain events for created, validated, challenged, promoted, quarantined, revoked and retired states.
- Implement outbox/inbox or equivalent exactly-once effects atop at-least-once delivery.
- Reject unknown versions, missing hashes, invalid roles and incompatible authority claims.
- Use asynchronous jobs for replay/training with deterministic status and artifact pointers.
- Maintain contract tests and golden vectors across Python, services and MQL5 mirrors.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `api_contract_catalog` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `domain_event` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `idempotency_record` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `job_manifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `schema_compatibility_report` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `service_authority_manifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `contract_test_vector` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- API and event contract compatibility.
- Idempotent retry correctness.
- Unknown/invalid request rejection.
- Artifact lineage across service boundaries.
- Job recovery and duplicate side-effect count.
- Golden-vector parity across implementations.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Two services assign different meaning to the same context field. |
| Failure | Retry creates duplicate outcome cubes or promotions. |
| Failure | Research API reaches live broker credentials. |
| Failure | Unknown schema fields are silently ignored. |
| Failure | Event ordering corrupts lifecycle state. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Every boundary has owner, schema, version and authority manifest.
- [ ] Retries are idempotent and tested.
- [ ] Research plane cannot invoke live execution.
- [ ] Compatibility failures block deployment.
- [ ] Golden vectors cover semantic and failure paths.

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
