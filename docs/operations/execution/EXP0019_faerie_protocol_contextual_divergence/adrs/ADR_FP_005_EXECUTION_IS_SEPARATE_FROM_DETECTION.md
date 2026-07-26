---
title: "ADR FP-005 - Execution Is Downstream of Detection"
tags: [exp0019, faerie-protocol, contextual-divergence, adr]
status: accepted
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# ADR FP-005 - Execution Is Downstream of Detection

## Decision

Execution, quota, risk, stop, target, and broker geometry consume confirmed context events. They do not recompute references, hunts, roles, or confirmation.

## Context

Recomputing detection inside execution creates inconsistent authority and prevents deterministic historical/live parity.

## Consequences

Execution receives immutable signal and policy records, produces entitlement/order-plan events, and preserves all failures without mutating the underlying signal.

## Rejected Alternatives

- Copy the monolithic FP101 implementation as the new base.
- Store business state in chart objects.
- Add hidden defaults for unresolved owner decisions.
- Modify shared cores with Faerie-only switch statements.

## Verification

- Dependency direction remains one-way.
- Earlier divergence-context regression suites remain unchanged and pass.
- FP golden fixtures exercise only public adapter surfaces.
- Contract and traceability checks link this ADR to modules and tests.

## Links

- [[../00_EXP0019_MOC|EXP0019 Master MOC]]
- [[../05_SHARED_CORE_REUSE_MATRIX|Shared Core Reuse Matrix]]
- [[../27_MQL5_MODULAR_ARCHITECTURE|MQL5 Modular Architecture]]
- [[../38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
