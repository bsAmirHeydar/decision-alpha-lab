---
title: "LCM-15 — Controlled Deletion and Root Hygiene"
status: proposed-reference
version: 2.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-15
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
partition_model: balanced-two-or-three-part
---
# LCM-15 — Controlled Deletion and Root Hygiene

## Master-phase purpose

Perform non-destructive structural reorganization and then the only approved destructive operation: exact, evidence-gated deletion.

## Approved balanced partition

This master phase remains one non-compensatory lifecycle gate, but implementation is divided into two or three bounded patches because a single monolithic delivery would combine too many evidence, implementation, parity, cutover or destructive responsibilities. The partition is intentionally moderate: it reduces interruption and rollback risk without creating dozens of administrative micro-phases.

1. [[LCM_15A_DELETION_CANDIDATE_INVENTORY_AND_REFERENCE_PROOF|LCM-15A — Deletion Candidate Inventory and Reference Proof]]
2. [[LCM_15B_ROOT_RELEASE_AND_DOCUMENTATION_REORGANIZATION|LCM-15B — Root, Release and Documentation Reorganization]]
3. [[LCM_15C_CONTROLLED_DELETION_AND_CLEAN_CLONE_VERIFICATION|LCM-15C — Controlled Deletion and Clean-Clone Verification]]

Required order: `LCM-15A → LCM-15B → LCM-15C`.

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

Only exact ledger-approved paths are deleted after reorganization and clean-clone verification; archive recovery remains possible.

## Master failure and rollback

A subphase failure does not authorize skipping to the next partition. The last accepted subphase output remains the recovery point. Rollback restores the exact prior handoff, including source files, locators, configuration, generated registries and relevant persistent state. The master phase may be re-entered only through a new versioned subphase attempt or approved ADR.

## Related controls

- [[06_REFINED_IMPLEMENTATION_ROADMAP]]
- [[PHASE_PARTITION_AND_PATCH_GRANULARITY_STANDARD]]
- [[SUBPHASE_HANDOFF_AND_CHECKPOINT_STANDARD]]
- [[BALANCED_PHASE_PARTITION_DECISION]]
