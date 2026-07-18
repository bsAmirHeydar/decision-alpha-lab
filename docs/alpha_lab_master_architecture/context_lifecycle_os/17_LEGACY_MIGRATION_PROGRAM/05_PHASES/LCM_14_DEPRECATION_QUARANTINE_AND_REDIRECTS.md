---
title: "LCM-14 — Deprecation, Quarantine and Redirects"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-14
---
# LCM-14 — Deprecation, Quarantine and Redirects

Remove legacy artifacts from active runtime and documentation paths while preserving reversibility, provenance and temporary compatibility.

## Claim ceiling

`DEPRECATION_AND_QUARANTINE_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-14.1 Deprecation registry

Record successor, warning, deprecation start, minimum compatibility window and removal gate.

### WP-14.2 Compatibility wrappers

Install minimal forwarding includes/imports and documentation stubs where active external consumers require them.

### WP-14.3 Quarantine bundle

Copy original bytes, hashes, mapping, parity, rollback and reference evidence outside active compile paths.

### WP-14.4 Active-reference verification

Scan code, configs, presets, docs, tests and generated assets for remaining consumers.

### WP-14.5 Restoration drill

Restore quarantined source and verify legacy compile/replay where tooling exists.

### WP-14.6 Quarantine aging

Start the non-destructive observation period and record new reference discoveries.

## Repository-specific target paths

- `lab/11_strategy_factory/migration/quarantine/<family>/<snapshot_id>/`
- `mql5/Include/AlphaLab/ContextOS/Compatibility/`
- `registry/legacy_context_migration/deprecations/`

## Mandatory verification

- quarantine manifest/hash
- no active include/import to original
- wrapper forwards exact identity/version
- restore drill
- quarantine path excluded from runtime build
- warning and successor link

## Hostile-review focus

- hidden external consumer
- wrapper accumulating new logic
- quarantine accidentally compiled
- lost binary/source evidence
- insufficient observation period

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Legacy originals are inactive and recoverable; compatibility is explicit; no deletion has occurred; active-reference scans are clean or blockers are listed.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
