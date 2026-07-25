---
id: UCPS-6308FE4C0B90
title: "UC-03 — Reorganize Physically"
type: stage
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
stage_id: UC-03
execution_order: 3
---
# UC-03 — Reorganize Physically

## Stage identity

- **Stage:** `UC-03`
- **Purpose:** Move files into the approved topology without intentionally changing business semantics.
- **Destructive authority:** Disabled

## Inputs

- UC-02 topology and disposition ledgers
- Characterization baseline
- Consumer graph

## Workstreams

1. Create final directory skeleton
2. Move production code with Git history preservation
3. Move tests and rename colliding modules
4. Relocate canonical documentation and release evidence
5. Separate authored, generated, runtime and historical artifacts
6. Rewrite imports, includes, paths and links using structured tools
7. Run regression and clean-clone checks after every wave
8. Remove empty and superseded directory shells only after verification

## Required outputs

- Physically organized repository
- Relocation ledger
- Path and import rewrite receipts
- Updated consumer graph
- Clean-clone report
- UC-04 handoff

## Non-compensatory exit gates

- [ ] Root files at or below twenty
- [ ] Zero production Python under lab
- [ ] Zero engine code under tools
- [ ] Zero broken import, include or documentation link
- [ ] No intentional semantic delta
- [ ] Characterization suite remains green

## Stop rules

The stage stops immediately on evidence loss, unexplained semantic drift, unknown destructive consumers, authority escalation, non-reproducible output or failed recovery. A stop produces a defect or incident record; it does not silently weaken the gate.

## Handoff rule

The next stage receives a hash-bound manifest, accepted exit report, unresolved-risk list and exact rollback/recovery instructions.
