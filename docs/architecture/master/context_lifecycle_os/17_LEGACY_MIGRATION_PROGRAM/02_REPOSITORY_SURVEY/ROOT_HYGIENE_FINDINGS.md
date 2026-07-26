---
title: "Root Hygiene Findings"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Root Hygiene Findings

The repository root currently contains 1,069 files. The initial classifier identified:

- 7 canonical root controls;
- 484 release-metadata candidates;
- 54 installer-script candidates;
- 9 commit-record candidates;
- 61 program artifacts requiring review;
- 453 unclassified root files requiring explicit disposition.

## Target

Keep only repository-wide controls at root. Move release bundles to `registry/history/releases/<program>/<release_id>/`, installer scripts to `tools/release/powershell/`, human release notes to `docs/history/delivery/releases/` and archived binary patches outside the active source tree or into an approved artifact store.

Root cleanup is performed in LCM-15 after locator and reference migration. Bulk moving these files earlier would break historical installation instructions and provenance links.
