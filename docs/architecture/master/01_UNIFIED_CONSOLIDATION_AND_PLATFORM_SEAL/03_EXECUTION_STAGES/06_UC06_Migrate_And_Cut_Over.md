---
id: UCPS-D5C5E830A065
title: "UC-06 — Migrate and Cut Over"
type: stage
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
stage_id: UC-06
execution_order: 6
---
# UC-06 — Migrate and Cut Over

## Stage identity

- **Stage:** `UC-06`
- **Purpose:** Move every active asset and consumer to canonical contracts and prove the platform with materially different Golden Contexts.
- **Destructive authority:** Enabled only after proof

## Inputs

- Mechanized platform
- Asset disposition ledger
- Internal and external consumer graph

## Workstreams

1. Run RTHP through universal path
2. Migrate a single-symbol Context without kernel changes
3. Migrate a path-dependent MQL5 Context without kernel changes
4. Migrate remaining Context, Setup, Treatment, visualizer and experiment families in waves
5. Rewrite Python, MQL5, CI, PowerShell, terminal and external consumers
6. Operate telemetry-backed compatibility shims temporarily
7. Run repository-wide acceptance and recovery
8. Resolve every BLOCKED asset into an explicit final disposition

## Required outputs

- Three Golden Context evidence packages
- Asset migration ledger
- Consumer cutover receipts
- Compatibility telemetry
- External environment evidence
- Zero-consumer report
- UC-07 handoff

## Non-compensatory exit gates

- [ ] Three Golden Contexts pass end-to-end
- [ ] All known assets have final disposition
- [ ] Zero unresolved internal consumer
- [ ] Zero unresolved external consumer
- [ ] Compatibility telemetry equals zero
- [ ] MQL5 compile, tester and parity matrices pass

## Stop rules

The stage stops immediately on evidence loss, unexplained semantic drift, unknown destructive consumers, authority escalation, non-reproducible output or failed recovery. A stop produces a defect or incident record; it does not silently weaken the gate.

## Handoff rule

The next stage receives a hash-bound manifest, accepted exit report, unresolved-risk list and exact rollback/recovery instructions.
