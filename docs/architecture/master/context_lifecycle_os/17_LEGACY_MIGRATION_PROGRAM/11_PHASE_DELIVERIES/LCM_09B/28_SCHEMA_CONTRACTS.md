---
title: "LCM-09B — Schema Contracts"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
---
# Schema Contracts

Closed Draft 2020-12 schemas cover packages, decisions, adapters, Factory registration, cases, traces, parity, blockers, dependencies, reports and handoff.

## Delivery artifacts

- `registry/history/lcm/setup_package_migrations/SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9`
- `LCM_09B_FILE_INDEX.txt`
- `LCM_09B_FILE_HASHES.sha256`
- `LCM_09B_QA_REPORT.json`


## Invariants

- No Setup semantics are inferred from filenames or static token counts.
- UNKNOWN and BLOCKED remain non-compensatory.
- Context semantics are read-only.
- Treatment, order and capital authority remain outside this phase.
