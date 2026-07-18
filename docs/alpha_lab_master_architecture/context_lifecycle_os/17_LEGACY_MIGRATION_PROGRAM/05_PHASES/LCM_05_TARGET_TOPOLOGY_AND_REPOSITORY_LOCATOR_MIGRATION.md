---
title: "LCM-05 — Target Topology and Repository Locator"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-05
---
# LCM-05 — Target Topology and Repository Locator

Approve the exact destination for every artifact class and the locator/redirect strategy that allows the repository to move without losing provenance or breaking consumers.

## Claim ceiling

`TARGET_TOPOLOGY_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-05.1 Package topology

Finalize Context, Setup, Treatment, visualizer, shared-engine, adapter, migration, release and documentation roots.

### WP-05.2 Dependency-direction enforcement

Define allowed imports/includes and prohibit domain-to-platform inversion, visualizer-to-domain mutation and Context-to-execution coupling.

### WP-05.3 Authored/generated boundary

Mark compiler-owned, report-generated and Obsidian-projection outputs. Generated files receive rebuild instructions and cannot be hand-edited.

### WP-05.4 Path migration map

Map every classified artifact to canonical target, compatibility wrapper, archive or quarantine.

### WP-05.5 Root relocation design

Design release registry and installer/document homes for the 1,069 root-level files without moving them yet.

### WP-05.6 Documentation successor map

Select canonical master documents and successor pages for duplicate or superseded namespaces.

## Repository-specific target paths

- `registry/legacy_context_migration/target_paths/`
- `docs/.../17_LEGACY_MIGRATION_PROGRAM/03_TARGET_ARCHITECTURE/`

## Mandatory verification

- no artifact class has two canonical homes
- dependency cycles are rejected
- generated paths cannot be canonical authority
- all old public paths have redirect or retirement plan
- target paths are Windows-safe and root-relative

## Hostile-review focus

- over-centralizing domain logic
- breaking MQL include conventions
- moving evidence into runtime paths
- creating a second competing architecture

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Every migration candidate has one approved target or explicit archive/quarantine outcome; no broad file movement has occurred.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
