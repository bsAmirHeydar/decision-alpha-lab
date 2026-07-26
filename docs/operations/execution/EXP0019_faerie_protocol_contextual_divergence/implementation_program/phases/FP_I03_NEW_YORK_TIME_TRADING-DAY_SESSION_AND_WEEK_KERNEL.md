---
title: "FP-I03 — New York Time, Trading-Day, Session, and Week Kernel"
tags: [exp0019, faerie-protocol, implementation-program, obsidian]
status: implemented_python_and_static_mql5_validated
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# FP-I03 — New York Time, Trading-Day, Session, and Week Kernel

## Mission

Implement exact New York conversion, DST, A/L/N ownership, trading-day boundaries, and Sunday-18:00-to-Friday-17:00 New York week semantics.

## Position in the program

- **Phase ID:** `FP-I03`
- **Depends on:** `FP-I02`
- **Primary product impact:** Shared context engine
- **Live execution authority:** `NONE`

## Scope

- NY conversion adapter
- DST transition table/math
- trading day key
- A/L/N session windows
- NY week key
- boundary ownership

## Explicit non-goals

- No prices or hunts
- No relation detection
- No rendering

## Entry criteria

- [ ] Previous phase is accepted and its file/hash manifest is available.
- [ ] All referenced contracts and dependency versions are exact.
- [ ] No unresolved regression exists in previous divergence contexts.
- [ ] Working tree changes unrelated to this phase are excluded from the patch.

## Planned deliverables

- FP_TimeAdapter.mqh
- FP_SessionCalendar.mqh
- FP_WeekCalendar.mqh
- time diagnostic/self-test


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

- [ ] DST spring/fall fixtures pass.
- [ ] every timestamp maps to one declared state.
- [ ] session and week boundaries are exact.
- [ ] broker timezone does not change NY identity.

- [ ] Phase file index and SHA-256 inventory validate.
- [ ] Documentation and implementation agree on versions and behavior.
- [ ] Rollback restores the previous accepted phase without deleting unrelated evidence.

## Handoff package

The handoff contains the exact public API, accepted tests, golden hashes, known limitations, performance baseline, changed file inventory, and one next-phase entry checklist. The next phase may not infer missing behavior from implementation details.

## Rollback boundary

Revert only files listed in this phase's file index. Persisted artifacts generated under the phase version are retained for audit, while incompatible checkpoints are ignored by the restored version.


## Implemented delivery

FP-I03 is implemented as a pure deterministic Python kernel plus an MQL5 mirror that reuses the accepted Daye New York conversion primitives. The delivered implementation includes:

- UTC-canonical instant handling and an explicit-offset broker adapter;
- deterministic US/New York DST rules for 2007–2099;
- unique, ambiguous, and nonexistent New York local-time resolution;
- ending-date trading-day labels;
- half-open A, L, N, daily-gap, and weekly intervals;
- semantic IDs and boundary-evidence hashes;
- adapters into the frozen FP-I02 WindowKey contract;
- 83 phase tests, 12 schemas, 20 conformance checks, and 12 exact boundary fixtures;
- MQL5 self-test and diagnostic entry points with no price, drawing, or trading authority.

### Canonical interval table

| State | New York interval | Ownership |
|---|---|---|
| A | `[18:00 previous date, 04:00 trading date)` | active session |
| L | `[04:00, 09:30)` | active session |
| N | `[09:30, 17:00)` | active session |
| Daily gap | `[17:00, 18:00)` | valid closed state; no session |
| NY week | `[Sunday 18:00, Friday 17:00)` | active weekly interval |
| Weekend closed | `[Friday 17:00, Sunday 18:00)` | no session/week ownership |

### Honest compile status

Python tests, schemas, vectors, boundary guards, and static MQL5 validation pass. Actual MetaEditor compile remains `pending_local_windows` until logs are produced on a Windows MT5 installation.

## Navigation

- [[../00_IMPLEMENTATION_PROGRAM_MOC|Implementation Program MOC]]
- [[../../00_EXP0019_MOC|EXP0019 Master MOC]]
- [[../../34_IMPLEMENTATION_ROADMAP|Implementation Roadmap]]
