---
title: "LCM-16 — Full Cutover and Program Closure"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-16
---
# LCM-16 — Full Cutover and Program Closure

Prove that active domain logic now enters ACL-OS through canonical packages and that the repository can be understood, built, tested, restored and evolved without the original migration conversation.

## Claim ceiling

`LEGACY_MIGRATION_CLOSURE_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-16.1 Canonical registry closure

Publish final Context, Setup, Treatment, visualizer, engine, adapter, alias, deprecation, quarantine and deletion registries.

### WP-16.2 Full-system verification

Run clean clone, Python compile/tests, schema validation, MQL5 compile/tester where available, golden replay, docs links, duplicate scan, forbidden API scan and manifest verification.

### WP-16.3 Architecture conformance

Verify dependency directions, package boundaries, generated/authored status and hidden-authority absence.

### WP-16.4 Rollback and recovery drill

Restore selected quarantined and deleted artifacts from approved archives and validate locator rollback.

### WP-16.5 Residual risk

Record unresolved external consumers, unavailable MT5 evidence, intentionally archived variants and accepted compatibility debt.

### WP-16.6 Closure decision

Issue CLOSED, CLOSED_WITH_RESIDUAL_RISK or REOPEN_REQUIRED. Closure never implies alpha or capital readiness.

## Repository-specific target paths

- `registry/legacy_context_migration/closure/`
- `reports/lcm/closure/`
- `docs/.../17_LEGACY_MIGRATION_PROGRAM/`

## Mandatory verification

- canonical locator completeness
- zero active unresolved legacy source
- full clean-checkout QA
- event/provenance verification
- rollback drill
- documentation self-sufficiency

## Hostile-review focus

- declaring closure from file movement
- unavailable MetaEditor/MT5 proof
- compatibility wrappers becoming permanent
- residual unknown external consumers

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

All active identities resolve through canonical ACL-OS packages; legacy residues are explicit archive/quarantine/compatibility assets; no hidden execution authority remains; closure limitations are honest.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
