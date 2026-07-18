---
title: "LCM-11 — Visualization and Object Lifecycle"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-11
---
# LCM-11 — Visualization and Object Lifecycle

Make all drawings deterministic projections of domain events and remove hidden signal/state authority from chart-object code.

## Claim ceiling

`VISUALIZATION_MIGRATION_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-11.1 Visual event contract

Define source identity, event, anchor bar/time/price, direction, style, ownership and lifecycle.

### WP-11.2 Object identity registry

Create deterministic instance-safe names and ownership prefixes. Resolve collisions among old prefixes.

### WP-11.3 Drawing extraction

Move line, zone, label, session box, dashboard and debug rendering out of detectors and treatments.

### WP-11.4 Lifecycle parity

Characterize create/update/delete, chart restart, timeframe change, history reload and indicator removal.

### WP-11.5 Variant preservation

Keep fixed-timeframe-close and host-chart-close drawing endpoints as explicit variants where approved.

### WP-11.6 Visual evidence

Produce anchor-level parity records and bounded screenshot review artifacts.

## Repository-specific target paths

- `lab/11_strategy_factory/visualizers/<visualizer_id>/`
- `mql5/Include/AlphaLab/ContextOS/Visualizers/<visualizer_id>/`

## Mandatory verification

- object name collision
- anchor time/price exactness
- restart and history expansion
- owned-prefix cleanup only
- multi-chart/multi-instance
- drawing disabled leaves domain outputs unchanged

## Hostile-review focus

- drawing function creating signals
- wrong symbol price drawn
- endpoint semantics changing
- deleting objects owned by another module
- performance collapse from full redraw

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Disabling visualization cannot change domain behavior; anchor and lifecycle parity pass; object ownership is deterministic.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
