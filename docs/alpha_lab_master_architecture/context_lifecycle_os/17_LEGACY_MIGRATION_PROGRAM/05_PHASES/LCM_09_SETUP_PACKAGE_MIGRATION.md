---
title: "LCM-09 — Setup Package Migration"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-09
---
# LCM-09 — Setup Package Migration

Standardize opportunity logic as independent Setup packages bound to canonical Context observations.

## Claim ceiling

`SETUP_PACKAGE_MIGRATION_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-09.1 Setup identity split

Separate variants by direction, confirmation timeframe, continuation/reversal anatomy, eligibility and expiry when differences are semantic.

### WP-09.2 Contract extraction

Author Context binding, eligibility, trigger, confirmation, invalidation, expiry, abstention and treatment-binding contracts.

### WP-09.3 State and entitlement

Separate Setup lifecycle and entitlement from execution quota or broker state.

### WP-09.4 Golden decision parity

Compare setup creation, suppression, no-trade, confirmation, cancellation, invalidation and reason codes.

### WP-09.5 Setup Factory registration

Register human-defined and bounded AI candidate exposure without granting promotion.

### WP-09.6 Consumer migration

Switch reports, visualizers and treatments to canonical Setup records incrementally.

## Repository-specific target paths

- `lab/11_strategy_factory/setups/<setup_id>/`
- `mql5/Include/AlphaLab/ContextOS/Setups/<setup_id>/`

## Mandatory verification

- context-binding integrity
- trigger/confirmation edge cases
- host-chart/fixed-timeframe variants
- invalidation and expiry
- abstention/no-trade
- no independent Context clock or broker API

## Hostile-review focus

- merging continuation and reversal variants
- confirmation on wrong candle
- quota consumption leaking into Setup
- visual suppression deleting raw evidence

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Each Setup has one canonical contract, preserved variants and exact approved decision traces; execution remains separate.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
