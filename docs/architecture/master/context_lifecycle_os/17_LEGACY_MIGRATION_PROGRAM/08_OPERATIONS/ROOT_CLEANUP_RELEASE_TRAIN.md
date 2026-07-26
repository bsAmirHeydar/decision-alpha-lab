---
title: "Root Cleanup Release Train"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, project-decision]
---
# Root Cleanup Release Train

## Train A — Registry preparation

Create `registry/history/releases`, `docs/history/delivery/releases` and `tools/release/powershell` conventions. Build a locator for every root release family. No root file moves.

## Train B — Exact historical mapping

For each root artifact identify program, release/phase, related patch, current consumers and historical installation references. Unknown artifacts remain at root with `ROOT_REVIEW_REQUIRED`.

## Train C — Non-breaking relocation

Move one program family at a time. Update file indexes, documentation and installer references. Provide temporary locator/redirect records. Do not combine with domain migration.

## Train D — Duplicate and stale release review

Compare identical release metadata, superseded installers and archived patch readmes. Preserve audit records even when operational copies are removed.

## Train E — Root closure

Allow only repository controls and explicitly approved human entry files at root. Run clean-clone, historical release lookup and exact path-reference scans.

## Prohibited shortcuts

- bulk wildcard move;
- broad root deletion;
- using filename pattern as proof of obsolescence;
- deleting commit messages or manifests needed for audit;
- retaining two active release registries after migration.
