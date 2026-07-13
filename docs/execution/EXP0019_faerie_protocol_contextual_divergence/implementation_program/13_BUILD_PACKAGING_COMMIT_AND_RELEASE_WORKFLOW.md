---
title: "Build, Packaging, Commit, and Release Workflow"
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
# Build, Packaging, Commit, and Release Workflow

## Per-phase release sequence

```text
implement phase
→ compile all changed entry points
→ run phase self-tests
→ run cumulative FP tests
→ run previous-context compatibility tests
→ update documentation/evidence
→ generate file index and hashes
→ build patch ZIP
→ verify patch on clean baseline
→ commit only indexed files
→ push
```

## Patch discipline

Each phase patch contains only files owned or modified by that phase. The patch root must be the repository root, not an extra wrapper directory.

Required release metadata:

- `EXP0019_FP_<PHASE>_FILE_INDEX.txt`
- `EXP0019_FP_<PHASE>_FILE_HASHES.sha256`
- `EXP0019_FP_<PHASE>_PATCH_MANIFEST.json`
- `EXP0019_FP_<PHASE>_QA_REPORT.json`
- `COMMIT_MESSAGE.md`

## Git staging rule

Only paths from the phase file index may be staged. Unrelated changes in the working tree remain unstaged.

## Versioning

- Shared-core contract change: increment shared-core version and rerun all dependent contexts.
- FP semantic change: increment context version and signal/config identity epoch.
- Indicator projection-only change: increment product/projection version without rewriting semantic IDs.
- Live execution policy change: increment execution policy and authorization manifest.
