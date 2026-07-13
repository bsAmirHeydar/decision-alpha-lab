---
title: "FP-I00 — Governance, Baseline Freeze, and Source-Control Harness"
tags: [exp0019, faerie-protocol, implementation-program, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# FP-I00 — Governance, Baseline Freeze, and Source-Control Harness

## Mission

Freeze the implementation baseline, source hashes, shared-core versions, owner decisions, open decision FP-DEC-012, and phase governance before code changes.

## Position in the program

- **Phase ID:** `FP-I00`
- **Depends on:** Frozen v2 documentation and repository baseline
- **Primary product impact:** Shared context engine
- **Live execution authority:** `NONE`

## Scope

- Repository baseline and clean status
- Source package and v2 documentation hashes
- Shared-core dependency inventory
- Context/product version policy
- Patch and rollback conventions

## Explicit non-goals

- No executable FP module is added
- No owner decision is inferred
- No shared core is modified

## Entry criteria

- [ ] Previous phase is accepted and its file/hash manifest is available.
- [ ] All referenced contracts and dependency versions are exact.
- [ ] No unresolved regression exists in previous divergence contexts.
- [ ] Working tree changes unrelated to this phase are excluded from the patch.

## Planned deliverables

- Baseline manifest
- dependency inventory
- governance self-check
- phase registry


## Engineering procedure

1. Freeze the phase-specific public contracts and identify all behavior-bearing fields.
2. Add compile-time enums/types before engine behavior.
3. Implement the smallest deterministic module behind an explicit interface.
4. Add module-local self-tests before integration.
5. Integrate only through the composition root; leaf modules may not reach upward into product entry points.
6. Add golden, negative, restart, and failure-injection fixtures relevant to the phase.
7. Compile every affected indicator/EA/test entry point in MetaEditor.
8. Run cumulative FP tests and previous-context compatibility tests.
9. Record telemetry/performance evidence when state volume or runtime work changes.
10. Update Obsidian documentation, file inventory, hashes, QA, commit message, and rollback scope.

## Required state and event evidence

| Evidence | Requirement |
|---|---|
| configuration/context hash | exact and visible in diagnostics |
| module version | included in manifest/checkpoint |
| semantic IDs | canonical and deterministic |
| state transitions | append-only or reproducible from event stream |
| reason codes | closed registry; no free-text-only failure |
| health state | READY/DEGRADED/BLOCKED with cause |
| test fixture ID | attached to golden/replay output |
| source data revision | recorded for replay-relevant phases |

## Failure behavior

- Missing or incompatible dependency: fail initialization or keep product `BLOCKED`; never guess.
- Missing M1/history: preserve data-incomplete evidence and block conclusions that require the data.
- Duplicate event: deduplicate by semantic identity and emit diagnostic evidence.
- Illegal transition: reject transition and fail the self-test.
- Checkpoint/version mismatch: discard checkpoint and perform deterministic rebuild.
- Performance overrun: preserve semantic processing, degrade noncritical projection, and report health.
- Regression in another context: stop phase acceptance.

## Test obligations

### Unit and contract

- Every enum/state/ID input validates.
- One behavior-bearing field change changes the required identity.
- Repeated identical input produces identical state/output.

### Golden and negative

- At least one positive golden path for every new semantic branch.
- At least one missing/ambiguous/invalid path.
- Duplicate/replay/restart path where state is persistent.

### Integration

- Nearest upstream and downstream contracts are exercised.
- No forbidden dependency or authority is imported.
- Previous-context compatibility remains green.

### Runtime and performance

- MetaEditor compile evidence.
- Strategy Tester or diagnostic runtime evidence where applicable.
- Incremental processing counters prove no accidental full-history loop.

## Acceptance criteria

- [ ] All source and decision hashes resolve.
- [ ] previous context tests are discoverable.
- [ ] phase file ownership is defined.

- [ ] Phase file index and SHA-256 inventory validate.
- [ ] Documentation and implementation agree on versions and behavior.
- [ ] Rollback restores the previous accepted phase without deleting unrelated evidence.

## Handoff package

The handoff contains the exact public API, accepted tests, golden hashes, known limitations, performance baseline, changed file inventory, and one next-phase entry checklist. The next phase may not infer missing behavior from implementation details.

## Rollback boundary

Revert only files listed in this phase's file index. Persisted artifacts generated under the phase version are retained for audit, while incompatible checkpoints are ignored by the restored version.

## Navigation

- [[../00_IMPLEMENTATION_PROGRAM_MOC|Implementation Program MOC]]
- [[../../00_EXP0019_MOC|EXP0019 Master MOC]]
- [[../../34_IMPLEMENTATION_ROADMAP|Implementation Roadmap]]
