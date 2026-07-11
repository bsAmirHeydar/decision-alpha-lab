---
title: "Phase 00 Charter and Gate"
tags: [strategy-factory, phase-00, governance]
status: canonical
---

# Phase 00 Charter and Gate

## Mission

The mission of Phase 00 is to make the current repository **legible, classifiable, and migratable** before the Strategy Factory kernel is allowed to exist. The phase treats the old repository as evidence. It does not assume that existing names, folder boundaries, or interfaces are correct merely because they exist.

## Questions Phase 00 must answer

1. Which capabilities already exist in working code?
2. Which capabilities exist only as documentation or empty scaffolding?
3. Which modules can be reused without semantic change?
4. Which modules must be adapted to a new contract?
5. Which strategy-specific engines must be wrapped rather than moved into the kernel?
6. Which capabilities have multiple competing implementations?
7. Is any module currently able to send or preflight a live order?
8. Can the repository be tested from a clean checkout?
9. What migration risks would invalidate later-phase assumptions?
10. Which implemented chain should act as the local foundation pilot?

## In scope

- Full repository inventory, excluding Git object internals.
- Text and binary artifact categorization.
- Empty-file and placeholder identification.
- Python class and callable discovery.
- Implicit contract map.
- Execution-authority scan.
- Duplicate-capability analysis.
- Migration classification.
- Test and compilation baseline.
- Risk register.
- Pilot selection.
- Phase 01 handoff.

## Out of scope

Phase 00 does not:

- define final Strategy Factory schemas;
- change L-rule or M0001 semantics;
- normalize timestamps;
- create the package skeleton;
- move cache files;
- fix legacy tests;
- add MQL5 runtime code;
- add paper or live execution;
- train a model;
- run a profitability study.

Those changes belong to later phases. Doing them here would contaminate the baseline we are trying to measure.

## Gate semantics

### `ACCEPTED`

All required evidence is present, no unclassified capital authority exists, the baseline test suite passes, and no blocking risk is deferred.

### `ACCEPTED_WITH_DEFERRED_REMEDIATIONS`

The baseline is complete and the next phase can proceed without private knowledge, but one or more defects are intentionally assigned to a later owner phase. This is the current result.

### `BLOCKED`

Any of the following blocks the phase:

- unidentified executable order authority;
- unclassified reusable module;
- missing required artifact;
- non-deterministic inventory;
- no explicit pilot decision;
- a critical assumption that Phase 01 cannot resolve from evidence.

## Current gate decision

The phase is accepted with deferred remediations because:

- no live-order call site was found;
- all 16 module groups are classified;
- three duplicate capability groups are explicitly resolved at the architectural level;
- 10 migration risks have assigned owner phases;
- 13 Phase 00 tests pass;
- the old repository pytest baseline fails for a known packaging reason;
- the local foundation pilot is explicit;
- the full EXP0017 and NDS repositories are absent from this snapshot and recorded as a later pilot dependency.

## Authority of this phase

Phase 00 may classify and document. It may add a read-only auditor and generated evidence. It may not rewrite old engines. Its output is authoritative for migration planning but not for market semantics.
