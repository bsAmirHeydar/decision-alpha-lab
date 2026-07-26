---
title: "Phase Delivery Contract and Definition of Done"
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
# Phase Delivery Contract and Definition of Done

Every implementation phase is a closed engineering delivery, not an informal coding session.

## Required phase artifacts

1. **Phase specification** with frozen scope and explicit non-goals.
2. **Code inventory** listing every added/modified file.
3. **Contract inventory** for types, enums, IDs, inputs, events, and reason codes.
4. **Unit/self-tests** for module-local behavior.
5. **Integration tests** at the nearest stable boundary.
6. **Golden fixtures** where deterministic replay is relevant.
7. **Failure injection** for missing data, duplicate events, restart, and dependency failure.
8. **Performance evidence** when the phase changes scanning, rendering, or memory.
9. **Documentation update** and Obsidian links.
10. **Patch metadata** with index, hashes, commit message, and rollback boundary.

## Standard phase gate

```text
Entry criteria satisfied
        ↓
Contracts frozen
        ↓
Implementation
        ↓
Static checks and MetaEditor compile
        ↓
Unit/self-tests
        ↓
Integration/golden/failure tests
        ↓
Documentation and evidence
        ↓
Independent patch and handoff
```

## Exit status taxonomy

| Status | Meaning |
|---|---|
| `PLANNED` | documented but not started |
| `IMPLEMENTING` | code under active change |
| `STATIC_VALIDATED` | structure/static gates pass; no runtime claim |
| `COMPILED` | MetaEditor compile evidence exists |
| `RUNTIME_VALIDATED` | self-tests or Strategy Tester evidence passes |
| `ACCEPTED` | all exit criteria pass and handoff is approved |
| `BLOCKED` | explicit dependency or owner decision prevents completion |

## Prohibited shortcuts

- Declaring a phase complete because code compiles.
- Using screenshots as the only semantic evidence.
- Reusing object names as signal identity.
- Mixing unrelated changes in the phase commit.
- Advancing while a compatibility regression is open.
