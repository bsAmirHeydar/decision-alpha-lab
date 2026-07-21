---
title: "LCM-13 — Wave Cutover, Dual Run and Consumer Switch"
status: implemented-reference
version: 2.0.0
updated: 2026-07-21
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-13
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
partition_model: balanced-two-or-three-part
---
# LCM-13 — Wave Cutover, Dual Run and Consumer Switch

## Master-phase purpose

Prove canonical and legacy behavior under dual run, switch consumers in bounded waves, and verify reversible cutover.

## Approved balanced partition

This master phase remains one non-compensatory lifecycle gate, but implementation is divided into two or three bounded patches because a single monolithic delivery would combine too many evidence, implementation, parity, cutover or destructive responsibilities. The partition is intentionally moderate: it reduces interruption and rollback risk without creating dozens of administrative micro-phases.

1. [[LCM_13A_DUAL_RUN_HARNESS_AND_MISMATCH_REGISTRY|LCM-13A — Dual-Run Harness and Mismatch Registry]]
2. [[LCM_13B_CONTROLLED_CONSUMER_WAVE_CUTOVER|LCM-13B — Controlled Consumer Wave Cutover]]
3. [[LCM_13C_ROLLBACK_DRILL_AND_CUTOVER_CLOSURE|LCM-13C — Rollback Drill and Cutover Closure]]

Required order: `LCM-13A → LCM-13B → LCM-13C`.

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

Eligible consumers resolve to canonical packages, every switch is reversible, and blocked consumers remain explicit on legacy paths.

## Master failure and rollback

A subphase failure does not authorize skipping to the next partition. The last accepted subphase output remains the recovery point. Rollback restores the exact prior handoff, including source files, locators, configuration, generated registries and relevant persistent state. The master phase may be re-entered only through a new versioned subphase attempt or approved ADR.

## Related controls

- [[06_REFINED_IMPLEMENTATION_ROADMAP]]
- [[PHASE_PARTITION_AND_PATCH_GRANULARITY_STANDARD]]
- [[SUBPHASE_HANDOFF_AND_CHECKPOINT_STANDARD]]
- [[BALANCED_PHASE_PARTITION_DECISION]]

## Accepted master-phase closure

LCM-13 is accepted at the reference-only claim ceiling through closure `CUTOVERCLOSE_0E477DA8D23F1B8DEB35DDD90B925F4F`. The consolidated gate switches 613 eligible consumers in 27 bounded waves, leaves 806 blocked consumers explicit on legacy, verifies rollback and deterministic forward recovery for every completed wave, and accounts for six persistent-state planes per wave. All 27 waves are `CLOSED_WITH_RESIDUAL_RISK`; none are `REOPEN_REQUIRED`. The only permitted next action is LCM-14A deprecation registration and minimal compatibility redirects; quarantine and deletion remain forbidden.
