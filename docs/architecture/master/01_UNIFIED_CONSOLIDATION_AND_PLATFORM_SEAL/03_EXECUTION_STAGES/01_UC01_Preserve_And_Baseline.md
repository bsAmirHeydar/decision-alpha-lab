---
id: UCPS-AFEEA3730362
title: "UC-01 — Preserve and Baseline"
type: stage
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
stage_id: UC-01
execution_order: 1
---
# UC-01 — Preserve and Baseline

## Stage identity

- **Stage:** `UC-01`
- **Purpose:** Freeze a complete, recoverable and behavior-aware baseline before any structural movement.
- **Destructive authority:** Disabled

## Inputs

- Current clean repository snapshot
- LCM discovery and migration evidence
- Git history and LFS objects
- Known terminal and external environment inventory

## Workstreams

1. Create immutable tag, archive branch, Git bundle and clean-checkout archive
2. Hash and classify every file and large object
3. Extract Python and MQL5 symbol inventories
4. Build import, include, documentation and external-consumer graphs
5. Create characterization fixtures for critical behavior
6. Record environment, toolchain and terminal identities
7. Prove full restoration into an isolated workspace

## Required outputs

- Preservation manifest
- Artifact and symbol inventories
- Dependency and consumer graphs
- Behavior baseline corpus
- Environment manifest
- Recovery drill receipt
- UC-02 handoff

## Non-compensatory exit gates

- [ ] 100% files hashed and classified
- [ ] 100% production symbols assigned
- [ ] No missing LFS object
- [ ] All critical behavior has characterization evidence
- [ ] Clean restore reproduces baseline
- [ ] No destructive change occurred

## Stop rules

The stage stops immediately on evidence loss, unexplained semantic drift, unknown destructive consumers, authority escalation, non-reproducible output or failed recovery. A stop produces a defect or incident record; it does not silently weaken the gate.

## Handoff rule

The next stage receives a hash-bound manifest, accepted exit report, unresolved-risk list and exact rollback/recovery instructions.
