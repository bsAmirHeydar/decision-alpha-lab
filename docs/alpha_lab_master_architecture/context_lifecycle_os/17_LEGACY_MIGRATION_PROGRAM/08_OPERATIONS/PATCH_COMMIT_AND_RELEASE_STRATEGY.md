---
title: "Patch, Commit and Release Strategy"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Patch, Commit and Release Strategy

Use separate commits for inventory, move-only, characterization, specification, adapter, behavioral refactor, cutover, quarantine and deletion. A commit that both moves and rewrites a large file destroys reviewability.

Every patch contains root-relative files, inventory, file index, hashes, manifest, QA report, commit message, installation guide and rollback. Staging uses `git add --pathspec-from-file` to avoid Windows command-line limits and never uses `git add .`.
