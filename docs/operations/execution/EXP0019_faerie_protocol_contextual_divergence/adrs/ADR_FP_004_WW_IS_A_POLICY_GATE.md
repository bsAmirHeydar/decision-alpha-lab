---
title: "ADR FP-004 - WW Detection and WW Policy Are Separate"
tags: [exp0019, faerie-protocol, contextual-divergence, adr]
status: accepted
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# ADR FP-004 - WW Detection and WW Policy Are Separate

## Decision

Generate WW as a normal contextual-divergence event, then resolve its effect on lower-relation eligibility in a separate weekly policy gate.

## Context

Raw detection must remain observable even when a policy suppresses execution. The owner later confirmed that WW is also independently tradeable, which strengthens rather than removes this separation.

## Consequences

WW detector, active-context resolver, lower-signal gate, and direct WW execution adapter are separate modules with separate evidence.

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
