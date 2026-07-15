---
title: "UCE-I19 — Prospective Stage Windows"
tags: [strategy-factory, uce-i19, production-operations, deployment]
status: implemented_reference_external_evidence_pending
doc_version: 1.0.0
last_updated: 2026-07-15
---
# Prospective Stage Windows

## Decision

Defines prospectively frozen paper, shadow, micro-live, limited-live, and production observation windows.

## Scope and non-goals

A window is invalidated by future selection, retroactive exclusions, missing sessions, changed generation, changed target, or unarchived incidents. The control is evaluated only against artifacts available at the decision cut. It does not fill missing fields, infer broker semantics, reinterpret a market setup, or convert a monitoring recommendation into execution authority.

## Authority and ownership

The semantic owner is the closed `operations_*` schema family and the `strategy_factory_operations_v3` package. The exact UCE-I18 `ReleaseManifest` remains the upstream authority ceiling. MQL5 files under `StrategyFactory/Operations` mirror deterministic guards and diagnostics; they contain no implicit order, broker, credential, filesystem-expansion, subprocess, or network authority. The locked execution adapter is the only component that may translate a valid cycle authorization into an already-approved broker action.

## Required inputs and known-time contract

- source commit, qualification-report hash, release-manifest hash, environment hash, generation hash, and rollback-generation hash;
- deployment-target hash covering broker server, account hashes, terminal instances, symbol allowlist, timezone, and capture time;
- operations-policy and risk-envelope hashes;
- event time, observation time, availability time, processing time, and evidence capture time where relevant;
- current lease, telemetry, reconciliation, incident, EOD, and operator-roster evidence.

Evidence observed after the evaluation cut cannot repair or authorize an earlier cycle. A missing timestamp, unknown schema major version, stale hash, unreadable artifact, or incompatible environment is retained as evidence and evaluated as pending or failed.

## Control sequence

1. Resolve exact immutable identities and reject partial or ambiguous bindings.
2. Validate schema closure, canonical hashes, timestamps, expiry, stage, target, and separation of duties.
3. Evaluate hard safety limits before degradable service objectives.
4. Reconcile reservations, intents, orders, fills, positions, cash, and generation state where applicable.
5. Produce a machine-readable decision with zero authority by default, explicit reason codes, evidence hashes, and expiry.
6. Preserve both success and failure evidence and hand the decision to the next typed boundary without side effects.

## Invariants

- No authority exists without an exact, unexpired I18 release, deployment plan, runtime lease, current health evidence, and exact reconciliation.
- Critical failures are non-compensatory and force zero incremental risk.
- Synthetic fixtures and static checks prove contracts only; they do not prove broker safety or market edge.
- Capital and stage may never increase automatically.
- Every state transition, approval, incident, and evidence item is immutable, hashed, and known-time ordered.

- The control described by this document cannot widen account, symbol, generation, stage, duration, or risk scope beyond its upstream manifest.

## Failure behavior

| Condition | Required control response | Durable evidence |
|---|---|---|
| Missing, corrupt, unsigned, unknown-major, or hash-mismatched input | `block` or `safe_halt`; zero incremental risk | gate result, reason code, raw artifact hash |
| Expired plan, lease, approval, roster, or release | deny authority immediately | expiry evaluation and lease/release identity |
| Environment, account, terminal, symbol, or generation mismatch | safe halt and incident review | target/reconciliation report |
| Stale heartbeat, stale features, duplicate/stale/unreserved action, or unsynchronized history | safe halt | telemetry snapshot and authorization record |
| Degradable latency, queue, memory, reject, or drift budget | derisk or hold according to policy | SLO measurement and policy hash |
| Open high/critical incident or failed reconciliation | safe halt; no new order authority | incident and reconciliation hashes |
| Attempted automatic capital increase or stage skip | reject request | ramp decision and approval audit |

## Evidence and telemetry

The minimum evidence record includes input identities, policy identity, evaluated time, status, decision, reason codes, evidence hashes, authority flags, maximum incremental risk, operator/approver identities where required, and limitations. Raw terminal and broker artifacts remain external and are referenced by immutable hash; secrets are excluded. Evidence must allow a reviewer to reproduce why authority was granted, reduced, held, or denied without the original conversation.

## Verification requirements

- deterministic repeated evaluation and canonical hash equality;
- boundary values at expiry, freshness, risk, loss, queue, latency, reject, drift, and count limits;
- negative tests for missing, future, stale, reordered, duplicate, corrupt, unsupported, and mismatched inputs;
- authority scans proving no socket, HTTP, subprocess, secret retrieval, or order APIs in the reference package and diagnostics;
- closed-schema validation and unknown-field rejection;
- Windows MetaEditor compilation and MT5 runtime evidence for external acceptance;
- broker/account/symbol/restart/reconciliation evidence for any live stage.

## Operator procedure

Before relying on this control, the operator verifies the exact plan and lease hashes, clock, environment, generation, broker connectivity, history synchronization, reconciliation freshness, incident state, risk headroom, and evidence destination. Any uncertainty is resolved by hold or safe halt, not by manual override. A human approval must cite the exact decision artifact and must expire when the cited scope changes.

## Acceptance statement

Repository acceptance means the deterministic reference contract, tests, schemas, static MQL5 boundaries, tools, documentation, and blocked fixtures are internally consistent. Production acceptance requires external evidence listed in [[45_FIRST_EXTERNAL_OPERATIONS_GOLDEN_RUN]], [[46_ACCEPTANCE_EVIDENCE_MATRIX]], and [[51_LIMITATIONS_RESIDUAL_RISK_AND_EXTERNAL_EVIDENCE]].

## Obsidian links

- [[00_UCE_I19_DELIVERY_MOC|UCE-I19 Delivery MOC]]
- [[29_POST_TRADE_BROKER_STATEMENT_RECONCILIATION|Previous control]]
- [[31_CAPITAL_TIER_LADDER|Next control]]
- [[47_SCHEMA_CODE_MQL5_TEST_AND_TOOL_CATALOG|Implementation Catalog]]
- [[48_OPERATOR_RUNBOOK|Operator Runbook]]
- [[53_CURRENT_PHASE_STATUS|Current Status]]
