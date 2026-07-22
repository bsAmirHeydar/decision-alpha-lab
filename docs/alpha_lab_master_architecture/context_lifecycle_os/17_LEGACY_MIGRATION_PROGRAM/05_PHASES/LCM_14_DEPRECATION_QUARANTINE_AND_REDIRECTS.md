---
title: "LCM-14 — Deprecation, Quarantine and Redirects"
status: in-progress-reference
version: 2.1.0
updated: 2026-07-21
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-14
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
partition_model: balanced-two-or-three-part
---
# LCM-14 — Deprecation, Quarantine and Redirects

## Master-phase purpose

Deactivate legacy paths through explicit deprecation, redirects and immutable quarantine while preserving restoration and observation.

## Approved balanced partition

This master phase remains one non-compensatory lifecycle gate, but implementation is divided into two or three bounded patches because a single monolithic delivery would combine too many evidence, implementation, parity, cutover or destructive responsibilities. The partition is intentionally moderate: it reduces interruption and rollback risk without creating dozens of administrative micro-phases.

1. [[LCM_14A_DEPRECATION_REGISTRY_AND_COMPATIBILITY_REDIRECTS|LCM-14A — Deprecation Registry and Compatibility Redirects]]
2. [[LCM_14B_QUARANTINE_OBSERVATION_AND_RETIREMENT_ELIGIBILITY|LCM-14B — Quarantine, Observation and Retirement Eligibility]]

Required order: `LCM-14A → LCM-14B`.

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

Legacy originals are inactive and recoverable in quarantine, compatibility is bounded, and retirement eligibility is evidence-based; no deletion occurs.

## Master failure and rollback

A subphase failure does not authorize skipping to the next partition. The last accepted subphase output remains the recovery point. Rollback restores the exact prior handoff, including source files, locators, configuration, generated registries and relevant persistent state. The master phase may be re-entered only through a new versioned subphase attempt or approved ADR.

## Related controls

- [[06_REFINED_IMPLEMENTATION_ROADMAP]]
- [[PHASE_PARTITION_AND_PATCH_GRANULARITY_STANDARD]]
- [[SUBPHASE_HANDOFF_AND_CHECKPOINT_STANDARD]]
- [[BALANCED_PHASE_PARTITION_DECISION]]


## Current master-phase checkpoint

LCM-14A is accepted under `DEPRECATION_B53138FCCDFD91CC595A818BD7153132` and emits LCM-14B handoff `sha256:e6cdd8272af462e3dbf29a148343e6921cadf8c7b6f748c5ce0a0f0d50e8b3f1`. The master phase remains OPEN: 136 documentation redirect identities may proceed to bounded quarantine observation and restoration drills, while 477 active-source identities are non-compensatorily blocked. LCM-14 has not authorized deletion.

## Closure — 2026-07-22

LCM-14 is closed by LCM-14A and LCM-14B. Deprecation and redirect evidence covers 613 identities; immutable observation quarantine covers the 136 documentation redirect identities; 477 active-source identities remain explicitly blocked. No deletion occurred. Next: LCM-15A through `sha256:beb66a4bb6792692608c4223763f7f88198e62d63a51b217436e1b456ab02cb8`.
