---
title: "Work Breakdown Structure and Task Ledger"
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
# Work Breakdown Structure and Task Ledger

## Purpose

The phase specifications define acceptance boundaries. This WBS defines the implementation units that can be assigned, coded, reviewed, tested, and committed without creating a hidden monolith.

## Task-size rule

A normal implementation task should produce one coherent contract or module plus tests. A task is too large when it:

- changes more than one state machine;
- mixes semantic logic and chart rendering;
- modifies a shared core and an FP product in the same unreviewed step;
- cannot be reverted without removing unrelated behavior;
- has no isolated golden or negative test.

## Work streams

| Stream | Scope | Primary phases |
|---|---|---|
| `GOV` | source freeze, policy, manifests, compatibility | I00–I01 |
| `CTR` | types, enums, IDs, configuration | I02 |
| `TIM` | NY time, sessions, week | I03 |
| `DAT` | M1 sync, gaps, revisions | I04 |
| `REF` | windows, references, selector | I05 |
| `SIG` | relation, hunt, candidate, confirmation, WW | I06–I08 |
| `LED` | ledger, arbitration, checkpoint | I09 |
| `IND` | indicator shell, projection, UI, alerts, release | I10–I13 |
| `DIA` | diagnostic EA and differential parity | I14 |
| `EXE` | risk, paper, live | I15–I16 |

## Task state model

```text
PROPOSED
→ CONTRACT_FROZEN
→ IMPLEMENTING
→ CODE_REVIEW
→ COMPILED
→ TESTED
→ EVIDENCE_ATTACHED
→ ACCEPTED
```

Any failed gate moves the task to `BLOCKED` with a reason code. A blocked task is never silently marked complete because a later phase appears to work.

## Required task fields

- Task ID and owning phase.
- Input contract and dependency versions.
- Exact files added/modified.
- Public API delta.
- State transitions/reason codes introduced.
- Unit, golden, negative, restart, and performance tests.
- Acceptance evidence path.
- Rollback path.

## Commit grouping

Commits follow task or small task-group boundaries. Indicator rendering, alert routing, panel interaction, and execution must never share an undifferentiated commit.

## Machine-readable ledger

The canonical task list is `fp_implementation_task_ledger.v1.csv`. It is a planning artifact; actual completion status must be updated only with attached evidence.
