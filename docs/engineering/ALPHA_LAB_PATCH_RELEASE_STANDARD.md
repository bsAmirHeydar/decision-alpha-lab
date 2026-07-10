---
id: AIEOS2-55252DCE4FEC
title: "Alpha Lab Patch and Release Standard"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab Patch and Release Standard

## Patch Unit

Every change is delivered as a bounded root-relative ZIP patch. It must not include unrelated repository files or `.git` internals.

## Required Patch Contents

```text
INSTALL_<PATCH_ID>.md
changed/added source files
changed/added tests
normative documentation
Obsidian MOC/cards/concepts when applicable
validation/rollback notes
```

## Install Command Standard

Installation instructions use Windows PowerShell and must:

1. `Expand-Archive -Force` into repository root.
2. Remove the ZIP after extraction.
3. Stage only an explicit file list or a deliberately bounded directory.
4. Never use `git add .` or `git add -A`.
5. Produce an atomic, detailed commit.

## Patch Manifest

Each patch records:

```text
identity and purpose
base version/commit
current versus desired behavior
files to add/modify/not touch
non-goals
preserved invariants
migration/compatibility
verification commands and results
rollback
residual risks
commit message
```

## Versioning

- Patch: compatible defect fix or documentation correction.
- Minor: additive feature or contract extension.
- Major: breaking schema/API/behavior change.
- Research findings do not automatically change production version.

## Hotfix Rule

A hotfix fixes the narrow failure first. Root-cause consolidation and broader cleanup become a separate patch unless required for safety. The hotfix must identify the failing compiler/runtime behavior and regression test.
