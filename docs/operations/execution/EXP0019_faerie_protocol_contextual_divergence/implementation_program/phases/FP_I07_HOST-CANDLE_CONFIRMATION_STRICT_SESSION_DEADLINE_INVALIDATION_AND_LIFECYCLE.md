---
title: "FP-I07 — Host-Candle Confirmation, Strict Session Deadline, Invalidation, and Lifecycle"
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
# FP-I07 — Host-Candle Confirmation, Strict Session Deadline, Invalidation, and Lifecycle

## Mission

Project candidates onto the resolved host confirmation timeframe, require candle close inside the owning check session, and implement immutable lifecycle transitions.

## Position in the program

- **Phase ID:** `FP-I07`
- **Depends on:** `FP-I06`
- **Primary product impact:** Shared context engine
- **Live execution authority:** `NONE`

## Scope

- host-close clock
- candidate pending store
- same-session deadline
- confirmation predicate
- invalidation/expiry
- lifecycle reducer

## Explicit non-goals

- No WW gate
- No quota/execution
- No chart-object state

## Entry criteria

- [ ] Previous phase is accepted and its file/hash manifest is available.
- [ ] All referenced contracts and dependency versions are exact.
- [ ] No unresolved regression exists in previous divergence contexts.
- [ ] Working tree changes unrelated to this phase are excluded from the patch.

## Planned deliverables

- FP_ConfirmationEngine.mqh
- FP_LifecycleEngine.mqh
- confirmation/lifecycle self-tests
- boundary-cross fixtures


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

- [ ] close after session end cannot confirm.
- [ ] replay and live close clocks agree.
- [ ] confirmed signal is immutable evidence.
- [ ] illegal transitions are rejected.

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
