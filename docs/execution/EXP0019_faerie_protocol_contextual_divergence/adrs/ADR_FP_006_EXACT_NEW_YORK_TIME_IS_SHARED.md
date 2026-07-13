---
title: "ADR FP-006 - Exact New York Time Is a Shared Service"
tags: [exp0019, faerie-protocol, contextual-divergence, adr]
status: accepted
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# ADR FP-006 - Exact New York Time Is a Shared Service

## Decision

DST-aware UTC/New York conversion is defined once in the shared time core. Faerie Protocol supplies only trading-day, session, and weekly interval policies.

## Context

Multiple ad hoc timezone engines create contradictory A/L/N/W ownership and DST defects.

## Consequences

All FP intervals are derived from the same timezone service and record timezone-rule version, UTC offset, and half-open boundaries.

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
