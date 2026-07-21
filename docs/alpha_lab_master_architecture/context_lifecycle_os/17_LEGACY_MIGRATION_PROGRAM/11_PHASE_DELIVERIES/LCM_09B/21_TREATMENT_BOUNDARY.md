---
title: "LCM-09B — Treatment Boundary"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
---
# Treatment Boundary

Setup core contains no routing, sizing, broker state or chart mutation. Each identity seeds an explicit LCM-10 dependency.

## Delivery artifacts

- `registry/legacy_context_migration/setup_package_migrations/SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9`
- `LCM_09B_FILE_INDEX.txt`
- `LCM_09B_FILE_HASHES.sha256`
- `LCM_09B_QA_REPORT.json`


## Invariants

- No Setup semantics are inferred from filenames or static token counts.
- UNKNOWN and BLOCKED remain non-compensatory.
- Context semantics are read-only.
- Treatment, order and capital authority remain outside this phase.
