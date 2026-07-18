---
title: "LCM-00 — Baseline Freeze and Governance"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-00
---
# LCM-00 — Baseline Freeze and Governance

Create the legally and technically recoverable starting point for the entire migration. No later parity or deletion claim is credible unless the original repository state, active branches, owners, exceptions and toolchain are frozen here.

## Claim ceiling

`BASELINE_AND_GOVERNANCE_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-00.1 Repository snapshot

Record source-control commit, branch, tags, uncommitted changes, ignored files relevant to runtime, submodules, large files and environment-dependent assets. Create a content manifest for every in-scope file and preserve exact SHA-256 values.

### WP-00.2 Authority and ownership

Create program owner, domain owner, migration engineer, parity reviewer, security reviewer, knowledge curator and release operator registers. Unknown ownership is a blocker, not a default assignment.

### WP-00.3 Change-control side lane

Define how urgent fixes that occur during migration enter the baseline. Each side-lane change receives an amendment ID, old/new hashes, affected identities, semantic classification and re-characterization requirement.

### WP-00.4 Rollback foundation

Create repository restoration instructions and rehearse restoration into a clean directory. Record which artifacts are stored in Git and which require an external artifact store.

### WP-00.5 Program constitution

Bind the LCM constitution, classification registry, state machine, claim ceiling, waiver rules and destructive-action prohibition.

## Repository-specific target paths

- `registry/legacy_context_migration/baselines/<baseline_id>/`
- `lab/11_strategy_factory/migration/registry/`
- `docs/.../17_LEGACY_MIGRATION_PROGRAM/01_GOVERNANCE/`

## Mandatory verification

- recompute every baseline hash
- restore a clean snapshot and compare path/hash set
- reject absolute paths and traversal
- prove an undeclared post-freeze file is not accepted as baseline
- verify role conflicts and missing owners fail closed

## Hostile-review focus

- untracked local MQL5 files outside the repository
- binary models or PDFs not stored reproducibly
- active hotfix branches diverging during freeze
- assuming file modification time is provenance

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

All in-scope files are recoverable and hash-bound; owners and reviewers are explicit; the side-lane amendment process is testable; no source file has been moved or deleted.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
