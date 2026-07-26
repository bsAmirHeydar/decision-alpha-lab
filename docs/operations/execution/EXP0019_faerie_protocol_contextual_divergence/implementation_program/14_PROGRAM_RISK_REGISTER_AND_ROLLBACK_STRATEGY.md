---
title: "Program Risk Register and Rollback Strategy"
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
# Program Risk Register and Rollback Strategy

## Principal risks

| Risk | Consequence | Control |
|---|---|---|
| copying FP101 monolith | duplicated semantics and poor performance | phase/file architecture and code review |
| changing shared core for FP only | regressions in other contexts | adapter-first compatibility harness |
| indicator-specific detector | indicator/EA disagreement | one engine and parity tests |
| chart objects used as state | restart and cleanup corruption | ledger/store source of truth |
| M1 gaps treated as no hunt | false signals | explicit data health and execution block |
| full replay every timer | terminal freeze | cursors, caches, dirty sets |
| visual suppression deletes evidence | audit loss | visible suppressed state and ledger retention |
| quota race | more than one entry per pair/session | atomic arbiter/reservation |
| open FP-DEC-012 guessed | live behavior not owner-approved | hard live gate |

## Rollback boundaries

- Every phase has a separate commit and file index.
- Reverting an indicator projection phase must not remove semantic ledger files.
- Reverting execution phases must leave the complete indicator functional.
- Shared-core extraction rollback must restore old adapters and pass previous-context fixtures.
- Persisted checkpoints include version headers; incompatible checkpoints are ignored and rebuilt, never coerced.
