---
title: "LCM-16 — Full Cutover and Program Closure"
status: in-progress-reference
version: 2.0.0
updated: 2026-07-23
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-16
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
partition_model: balanced-two-or-three-part
---
# LCM-16 — Full Cutover and Program Closure

## Master-phase purpose

Run full closure evidence, recovery drills and final ledger publication, then issue an honest evidence-bounded program decision.

## Approved balanced partition

This master phase remains one non-compensatory lifecycle gate, but implementation is divided into two or three bounded patches because a single monolithic delivery would combine too many evidence, implementation, parity, cutover or destructive responsibilities. The partition is intentionally moderate: it reduces interruption and rollback risk without creating dozens of administrative micro-phases.

1. [[LCM_16A_FULL_REGRESSION_MQL5_MATRIX_PARITY_AND_SECURITY_AUDIT|LCM-16A — Full Regression, MQL5 Matrix, Parity and Security Audit]]
2. [[LCM_16B_RECOVERY_DRILL_FINAL_LEDGER_AND_PROGRAM_CLOSURE|LCM-16B — Recovery Drill, Final Ledger and Program Closure]]

Required order: `LCM-16A → LCM-16B`.

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

The final evidence set supports CLOSED, CLOSED_WITH_RESIDUAL_RISK or REOPEN_REQUIRED without implying alpha, production or capital readiness.

## Master failure and rollback

A subphase failure does not authorize skipping to the next partition. The last accepted subphase output remains the recovery point. Rollback restores the exact prior handoff, including source files, locators, configuration, generated registries and relevant persistent state. The master phase may be re-entered only through a new versioned subphase attempt or approved ADR.

## Related controls

- [[06_REFINED_IMPLEMENTATION_ROADMAP]]
- [[PHASE_PARTITION_AND_PATCH_GRANULARITY_STANDARD]]
- [[SUBPHASE_HANDOFF_AND_CHECKPOINT_STANDARD]]
- [[BALANCED_PHASE_PARTITION_DECISION]]
## Current master-phase state — 2026-07-23

LCM-16A has an implemented, internally valid audit package, but its non-compensatory closure decision is `BLOCKED`. LCM-16B recovery-drill preparation is allowed; final program closure remains forbidden until real MetaEditor, Strategy Tester/golden replay, terminal parity and external-consumer evidence resolve the mandatory unknowns and the Git LFS evidence objects are materialized in the execution checkout.

