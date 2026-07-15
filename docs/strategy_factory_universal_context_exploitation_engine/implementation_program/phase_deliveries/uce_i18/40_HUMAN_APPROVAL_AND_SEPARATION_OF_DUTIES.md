---
title: "UCE-I18 — Human Approval and Separation of Duties"
tags: [strategy-factory, uce-i18, production-qualification, release]
status: implemented_reference_external_evidence_pending
doc_version: 1.0.0
last_updated: 2026-07-15
---
# Human Approval and Separation of Duties

## Decision

Separates builder, reviewer, approver and operator where feasible; approval ID, scope, expiry and revocation are immutable.



## Authority and contract

The semantic owner is the closed `qualification_*` schema family and the `strategy_factory_qualification_v3` package. MQL5 mirrors are conformance and diagnostic surfaces; they do not gain implicit order, broker or network authority. Any stage transition requires a machine-readable gate result and a human-approved release manifest where policy requires approval.

## Inputs and known-time requirements

- exact source commit and root-relative file inventory;
- immutable environment fingerprint and broker/symbol specification hashes;
- evidence timestamps distinguishing event, observation, availability and processing time;
- upstream I17 runtime, allocation, reservation and limitation hashes;
- explicit policy version and required-case inventory.

Evidence observed after a decision cut cannot retroactively qualify an earlier action. Missing, stale, reordered, corrupt or incompatible evidence is retained with a reason code and cannot be converted to pass by an aggregate score.

## Invariants

1. No release authority exists when a critical gate is `fail` or `pending`.
2. No action may be emitted after restart until generation, reservation, intent, order and position state reconcile.
3. Compile, parity, soak, chaos, security, paper, micro-live and rollback gates are non-compensatory.
4. Synthetic fixtures prove contract behavior only; they do not prove broker safety or market edge.
5. Every activation is bounded by stage, account, expiry, risk, generation and rollback identity.

## Failure behavior

| Condition | Required response | Durable evidence |
|---|---|---|
| Evidence missing or unreadable | hold/block; no default pass | gate result and reason code |
| Hash, signature or schema mismatch | block and preserve artifact | integrity report |
| Reconciliation mismatch | engage kill/safe halt | reconciliation and incident record |
| Hard budget exceeded | fail the gate | budget measurement |
| Approval absent or expired | deny live authority | release ledger |
| Rollback cannot be proven | deny activation | rollback drill report |

## Verification

The executable suite must include deterministic repeatability, boundary values, negative fixtures, future-read and event-order tests, schema closure, authority-denial scans, and MQL5 diagnostic compilation on the supported Windows terminal. External evidence must be archived without secrets and referenced by immutable hash.

## Obsidian links

- [[00_UCE_I18_DELIVERY_MOC|UCE-I18 Delivery MOC]]
- [[03_QUALIFICATION_STATE_MACHINE|Qualification State Machine]]
- [[43_ACCEPTANCE_EVIDENCE_MATRIX|Acceptance Evidence Matrix]]
- [[44_OPERATOR_RUNBOOK|Operator Runbook]]
- [[47_LIMITATIONS_RESIDUAL_RISK_AND_POST_I18_HANDOFF|Limitations and Handoff]]

