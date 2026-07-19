---
title: "LCM-09 — Setup Package Migration"
status: proposed-reference
version: 2.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-09
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
partition_model: balanced-two-or-three-part
---
# LCM-09 — Setup Package Migration

## Master-phase purpose

Standardize opportunity logic as canonical Setup packages bound only to canonical Context observations, with variants and abstention preserved.

## Approved balanced partition

This master phase remains one non-compensatory lifecycle gate, but implementation is divided into two or three bounded patches because a single monolithic delivery would combine too many evidence, implementation, parity, cutover or destructive responsibilities. The partition is intentionally moderate: it reduces interruption and rollback risk without creating dozens of administrative micro-phases.

1. [[LCM_09A_SETUP_INVENTORY_FAMILY_REGISTRY_AND_CANONICAL_CONTRACT_FREEZE|LCM-09A — Setup Inventory, Family Registry and Canonical Contract Freeze]]
2. [[LCM_09B_SETUP_MIGRATION_SETUP_FACTORY_BINDING_AND_BEHAVIORAL_PARITY|LCM-09B — Setup Migration, Setup Factory Binding and Behavioral Parity]]

Required order: `LCM-09A → LCM-09B`.

A completed subphase does not mean the master phase has passed. The master phase closes only after the final subphase handoff and the master acceptance gate are accepted.

## Partition invariants

- Subphase boundaries may reduce patch size but may not weaken evidence, ownership, known-time, parity, security, rollback or documentation requirements.
- An upstream UNKNOWN remains UNKNOWN downstream unless new evidence resolves it.
- No subphase may infer authority omitted from its handoff.
- Move, semantic refactor, consumer cutover, quarantine and deletion are separated according to the refined roadmap.
- Registries remain append-only or version-superseded; historical decisions are not overwritten.
- A failed subphase leaves the master phase open and downstream subphases blocked.

## Master entry contract

- Exact accepted handoff from the preceding master phase.
- Current baseline and all approved amendments.
- Closed identity/ownership/locator registries required by scope.
- Named domain owner, migration owner and independent reviewer.
- Explicit scope, non-goals, claim ceiling, allowed actions and forbidden actions.
- Clean or recorded working-tree state and rollback point.

## Master artifacts

- Master phase manifest linking all subphase manifests and digests.
- Consolidated acceptance-gate report.
- Consolidated blocker, UNKNOWN, variance and residual-risk registers.
- Final registry snapshots created by the phase.
- Master handoff that permits only the next master phase.

## Master acceptance gate

Every active Setup decision path is canonical or blocked, variants are preserved, and Setup Factory registration carries no promotion or execution authority.

## Master failure and rollback

A subphase failure does not authorize skipping to the next partition. The last accepted subphase output remains the recovery point. Rollback restores the exact prior handoff, including source files, locators, configuration, generated registries and relevant persistent state. The master phase may be re-entered only through a new versioned subphase attempt or approved ADR.

## Related controls

- [[06_REFINED_IMPLEMENTATION_ROADMAP]]
- [[PHASE_PARTITION_AND_PATCH_GRANULARITY_STANDARD]]
- [[SUBPHASE_HANDOFF_AND_CHECKPOINT_STANDARD]]
- [[BALANCED_PHASE_PARTITION_DECISION]]
