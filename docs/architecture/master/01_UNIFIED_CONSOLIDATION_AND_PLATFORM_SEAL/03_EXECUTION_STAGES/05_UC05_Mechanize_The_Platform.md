---
id: UCPS-DF59560BAC39
title: "UC-05 — Mechanize the Platform"
type: stage
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
stage_id: UC-05
execution_order: 5
---
# UC-05 — Mechanize the Platform

## Stage identity

- **Stage:** `UC-05`
- **Purpose:** Replace prompt-dependent and project-specific workflows with contracts, compilers, one lifecycle and one operator interface.
- **Destructive authority:** Disabled

## Inputs

- Unified engine
- Approved Context contract
- RTHP behavior baseline

## Workstreams

1. Implement Context Wizard and closed-schema intake
2. Implement universal Context compiler
3. Generate state machines, bindings, tasks, tests, docs and terminal contracts
4. Implement one lifecycle state engine
5. Implement one CLI and status/explain commands
6. Implement extension manifests and conformance
7. Constrain AI to typed proposal slots
8. Migrate RTHP-specific shared behavior into universal services

## Required outputs

- Context SDK and templates
- Universal compiler
- Generated artifact catalog
- CLI and operator interface
- AI proposal schemas
- Extension SDK
- Mechanized RTHP package
- UC-06 handoff

## Non-compensatory exit gates

- [ ] RTHP can be regenerated from authored sources
- [ ] Generated outputs are deterministic
- [ ] No manual edits in generated artifacts
- [ ] No RTHP conditional in shared engine
- [ ] Lifecycle transition requires evidence
- [ ] Standard Context work requires no architecture prompt

## Stop rules

The stage stops immediately on evidence loss, unexplained semantic drift, unknown destructive consumers, authority escalation, non-reproducible output or failed recovery. A stop produces a defect or incident record; it does not silently weaken the gate.

## Handoff rule

The next stage receives a hash-bound manifest, accepted exit report, unresolved-risk list and exact rollback/recovery instructions.
