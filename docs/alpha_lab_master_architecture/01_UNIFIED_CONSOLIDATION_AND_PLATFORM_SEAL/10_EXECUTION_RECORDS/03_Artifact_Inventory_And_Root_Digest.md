---
id: UCPS-UC01-ARTIFACTS-DC91AD2B
title: "Artifact Inventory and Repository Root Digest"
type: implementation_standard
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - inventory
  - hashing
  - artifacts
---
# Artifact Inventory and Repository Root Digest

Every tracked or non-ignored untracked repository file receives a total record containing path, SHA-256, byte size, object type, mode, suffix, language, artifact category, lifecycle classification, authorship class, owner domain, critical domains, criticality, Git status and Git LFS state.

## Root digest

The repository root digest is computed over sorted canonical lines:

```text
<file-sha256> <byte-size> <repository-relative-path>
```

The baseline output directory is excluded to prevent self-reference. Transient caches and `.git` are outside scope.

## UC-01 disposition discipline

Every artifact disposition is fixed to `UNASSESSED_UNTIL_UC02`. UC-01 cannot classify an artifact for deletion, movement, merge or retirement.

## Storage

The complete inventory is stored as deterministic `artifact_inventory.jsonl.gz`; the readable summary records total files, bytes, languages, categories, owner domains, criticality, top-level distribution and unresolved Git LFS pointers.
