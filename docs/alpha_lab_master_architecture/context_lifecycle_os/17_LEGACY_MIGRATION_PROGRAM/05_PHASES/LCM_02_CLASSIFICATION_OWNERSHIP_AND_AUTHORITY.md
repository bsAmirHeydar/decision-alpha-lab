---
title: "LCM-02 — Classification, Ownership and Authority"
status: implemented-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-02
---
# LCM-02 — Classification, Ownership and Authority

Decide what each artifact is, who owns its meaning and which migration disposition is permitted. This phase converts survey candidates into governed records but does not yet assign final canonical behavior.

## Claim ceiling

`CLASSIFICATION_AND_OWNERSHIP_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-02.1 Artifact role classification

Assign Context, Setup, Treatment, visualizer, platform adapter, execution adapter, shared primitive, research, diagnostic, platform kernel, generated projection, source evidence or release metadata.

### WP-02.2 Migration disposition

Assign exactly one primary disposition such as KEEP_CANONICAL, WRAP_LEGACY, REWRITE_WITH_PARITY, QUARANTINE_UNCERTAIN or SECURITY_RESTRICTED.

### WP-02.3 Ownership resolution

Bind semantic owner, code owner, documentation owner and security reviewer. Record owner evidence rather than inferring ownership from commit authorship.

### WP-02.4 Activity and reachability status

Classify active runtime, active research, test-only, documentation-only, generated, archived or unknown. Unknown remains blocked from deletion.

### WP-02.5 Authority boundary

Identify every artifact that can influence order requests, capital, broker state, file persistence, external models or network egress.

### WP-02.6 Unresolved queue

Create explicit work queues for unknown owner, ambiguous role, conflicting specifications and security-sensitive source.

## Repository-specific target paths

- `registry/legacy_context_migration/artifacts/`
- `registry/legacy_context_migration/owners/`
- `registry/legacy_context_migration/unresolved/`

## Mandatory verification

- reject multiple primary dispositions
- reject active artifact without semantic owner
- reject SECURITY_RESTRICTED downgrade without security approval
- prove generated projection cannot be selected as canonical doctrine
- verify platform kernel assets are protected from domain migration

## Hostile-review focus

- treating experiment ID as one Context
- confusing anatomy experts with production hosts
- classifying shared utilities from their folder rather than behavior
- silent ownership assumptions

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Every active candidate is owned and classified or explicitly blocked; all security-sensitive paths are isolated; no merge, move or deletion has been authorized.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.

## Implementation record

Reference implementation is delivered under `tools/strategy_factory/lcm/lcm_02`, machine registries under `registry/legacy_context_migration/lcm_02`, and immutable classification packages under `registry/legacy_context_migration/classifications`. See [[LCM02_DEFINITION_OF_DONE]] and [[LCM02_TO_LCM03_HANDOFF_CONTRACT]].
