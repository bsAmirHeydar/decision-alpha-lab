---
title: "LCM-09B — Entry Binding"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
---
# Entry Binding

The sole authoritative entry is LCM-09A handoff `sha256:9010023f1b182049cc9f7e0601689827c062f2dbb15e21a98d652744c625d2fb` and freeze `SETUPFREEZE_8638449DF9A774634FE9B8F9E17EF891`.

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
