---
title: "LCM-06 — Migration Framework and Compatibility Layer"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-06
---
# LCM-06 — Migration Framework and Compatibility Layer

Implement the reusable machinery required to migrate many Context families consistently rather than hand-crafting every move.

## Claim ceiling

`MIGRATION_FRAMEWORK_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-06.1 Migration packet validator

Validate identities, owners, source hashes, status transitions, paths, claim ceilings and evidence references.

### WP-06.2 Alias and locator resolver

Resolve canonical artifacts and compatibility aliases with closed version rules.

### WP-06.3 Trace normalization and comparator

Normalize MQL/Python traces, compare hard and soft parity dimensions, and produce reason-coded mismatch reports.

### WP-06.4 Compatibility adapter interfaces

Define legacy-to-canonical Context, Setup, visual and treatment adapters that cannot expand authority.

### WP-06.5 Move-only and redirect tooling

Generate reviewed `git mv` plans, MQL include wrappers and Obsidian redirect stubs without mixing semantic edits.

### WP-06.6 Quarantine and deletion validators

Verify inactive references, preservation bundles and non-compensatory deletion gates.

### WP-06.7 Reference fixtures

Test the framework with synthetic simple, ambiguous, missing-owner, future-aware and security-sensitive migration packets.

## Repository-specific target paths

- `tools/strategy_factory/lcm/`
- `lab/11_strategy_factory/migration/_templates/`
- `registry/history/lcm/schemas/`
- `lab/11_strategy_factory/migration/tests/`

## Mandatory verification

- schema/property tests
- invalid transition rejection
- path traversal/symlink rejection
- deterministic trace normalization
- hard mismatch cannot be waived as soft
- adapter cannot enable execution
- atomic publication and clean-overlay install

## Hostile-review focus

- framework becoming a second ACL-OS
- permissive defaults
- adapter semantics drifting from package contract
- tooling modifying generated or source evidence

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Framework passes reference and hostile tests, produces deterministic packets/reports, and has no domain-specific or execution authority.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
