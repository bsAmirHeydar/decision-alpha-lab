---
title: "LCM-15 — Controlled Deletion and Root Hygiene"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-15
---
# LCM-15 — Controlled Deletion and Root Hygiene

Perform the only intentionally destructive phase: remove artifacts that have passed every non-compensatory gate and relocate root clutter through approved locators.

## Claim ceiling

`CONTROLLED_DELETION_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-15.1 Deletion eligibility evaluation

Verify successor/archive, mapping, zero references, parity, approvals, quarantine, rollback, retained evidence and clean-clone status.

### WP-15.2 Root release migration

Move phase inventories, hashes, manifests and QA records to registry releases; installers to tools; release notes to docs; large patches to approved storage.

### WP-15.3 Duplicate documentation removal

Delete only exact duplicate trees whose canonical copy, redirects and external-link analysis are complete.

### WP-15.4 Dead code deletion

Remove quarantined files approved by ledger using explicit pathspecs.

### WP-15.5 Post-delete verification

Re-run references, compile/test/replay, Obsidian links, manifests, package installation and restoration from archive.

### WP-15.6 Deletion ledger publication

Record every deleted path/hash, reason, successor/archive, approvals and recovery location.

## Repository-specific target paths

- `registry/legacy_context_migration/deletions/`
- `registry/releases/`
- `tools/release/powershell/`
- `docs/releases/`

## Mandatory verification

- all deletion gates true
- exact path list review
- no `git add .` or broad wildcard delete
- clean clone
- full reference scan
- archive restore sample
- post-delete manifest

## Hostile-review focus

- irreversible loss
- external links unknown
- historical installer breakage
- case-sensitive/insensitive mismatch
- deleting source evidence mistaken for duplicate

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Only ledger-approved paths were removed; root contains only approved controls; all active builds/docs resolve; archive and rollback evidence remain intact.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
