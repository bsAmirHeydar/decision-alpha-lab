---
id: UCPS-EEE898CC3D72
title: "UC-02 Operator Runbook"
type: execution-record
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-24
updated: 2026-07-24
tags:
  - consolidation
  - uc02
  - authority-freeze
---
# UC-02 Operator Runbook

## Preconditions

UC-01 must be `ACCEPTED`, `uc02_authorized=true`, the worktree must be clean and Git LFS evidence must remain materialized.

## Execution order

1. verify the static patch and contract hashes;
2. run direct UC-02 tests;
3. build the authority package from the accepted UC-01 baseline;
4. qualify contracts, guards, deterministic rebuild, repository policy, Obsidian and MQL5 static compatibility;
5. finalize the non-compensatory decision;
6. verify the accepted authority package;
7. stage exactly the generated commit index;
8. commit and push.

## Failure handling

A failed build or gate does not authorize manual edits to generated ledgers. Correct the classifier, contract or source defect, remove the incomplete authority package and rebuild from the accepted baseline.

## Rollback

UC-02 is add-only. Before commit, remove its indexed paths. After commit, revert the UC-02 commit. The UC-01 baseline and pre-consolidation preservation refs remain untouched.
