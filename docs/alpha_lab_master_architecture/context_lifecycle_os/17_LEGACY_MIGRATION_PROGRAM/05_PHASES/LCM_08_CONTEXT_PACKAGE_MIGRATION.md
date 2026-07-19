---
title: "LCM-08 — Context Package Migration"
status: proposed-reference
version: 2.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-08
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
partition_model: balanced-two-or-three-part
---
# LCM-08 — Context Package Migration

## Master-phase purpose

Produce canonical, evidence-bound Context packages for the entire active portfolio without silently changing causal-time, state, occurrence or reference semantics.

## Approved balanced partition

This master phase remains one non-compensatory lifecycle gate, but implementation is divided into two or three bounded patches because a single monolithic delivery would combine too many evidence, implementation, parity, cutover or destructive responsibilities. The partition is intentionally moderate: it reduces interruption and rollback risk without creating dozens of administrative micro-phases.

1. [[LCM_08A_CONTEXT_PORTFOLIO_FREEZE_RISK_CLASSIFICATION_AND_PILOT_SELECTION|LCM-08A — Context Portfolio Freeze, Risk Classification and Pilot Selection]]
2. [[LCM_08B_PILOT_CONTEXT_MIGRATION_COMPATIBILITY_ADAPTER_AND_BEHAVIORAL_PARITY|LCM-08B — Pilot Context Migration, Compatibility Adapter and Behavioral Parity]]
3. [[LCM_08C_CONTEXT_WAVE_MIGRATION_AND_CONTEXT_PORTFOLIO_CLOSURE|LCM-08C — Context Wave Migration and Context Portfolio Closure]]

Required order: `LCM-08A → LCM-08B → LCM-08C`.

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

Every active Context identity has a canonical package with accepted parity or an explicit blocking/archive disposition; no active consumer cutover is implied.

## Master failure and rollback

A subphase failure does not authorize skipping to the next partition. The last accepted subphase output remains the recovery point. Rollback restores the exact prior handoff, including source files, locators, configuration, generated registries and relevant persistent state. The master phase may be re-entered only through a new versioned subphase attempt or approved ADR.

## Related controls

- [[06_REFINED_IMPLEMENTATION_ROADMAP]]
- [[PHASE_PARTITION_AND_PATCH_GRANULARITY_STANDARD]]
- [[SUBPHASE_HANDOFF_AND_CHECKPOINT_STANDARD]]
- [[BALANCED_PHASE_PARTITION_DECISION]]
