---
title: "ADR FP-001 - Faerie Protocol Is a Context Adapter over Fixed Cores"
tags: [exp0019, faerie-protocol, contextual-divergence, adr]
status: accepted
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# ADR FP-001 - Faerie Protocol Is a Context Adapter over Fixed Cores

## Decision

Implement Faerie Protocol as a context-policy layer. Do not inject A/L/N/WW conditions into the shared divergence kernels.

## Context

The project already has tested time, reference, hunt, divergence, visual, ledger, risk, and execution primitives. Context-specific branching inside those cores would couple unrelated divergence families and make regression evidence unreliable.

## Consequences

Faerie modules depend on public shared-core interfaces. Shared cores do not depend on Faerie modules. Any generic core extension requires compatibility tests for every earlier divergence context.

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
