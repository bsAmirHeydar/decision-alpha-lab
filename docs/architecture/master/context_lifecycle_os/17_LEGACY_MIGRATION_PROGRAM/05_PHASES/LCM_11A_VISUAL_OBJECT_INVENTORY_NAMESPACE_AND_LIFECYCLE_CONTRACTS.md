---
title: "LCM-11A — Visual Object Inventory, Namespace and Lifecycle Contracts"
status: implemented-reference
version: 1.1.0
updated: 2026-07-21
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-11A
master_phase: LCM-11
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-11A — Visual Object Inventory, Namespace and Lifecycle Contracts

## Purpose

Inventory every chart and report projection, assign deterministic ownership namespaces, and freeze object lifecycle and anchor semantics before visual implementation changes.

## Claim ceiling

`LCM_11A_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- MQL5 chart objects, buffers, labels, panels, session boxes, divergence lines, markers and report projections.
- Object naming, creation, update, deletion, restart and history-reload behavior.
- Source Context/Setup/Treatment event bindings.

## Explicit non-goals

- No broad redraw rewrite.
- No visual style cleanup that changes timing or evidence.
- No signal generation inside visualizer.

## Entry contract

- Canonical Context, Setup and Treatment event contracts.
- LCM-01 visualization surface.
- LCM-04 visual traces.
- LCM-05 visualizer target paths.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Object inventory

- Record object type, source path, prefix, chart scope, symbol, timeframe, anchors, style, update policy and delete policy.
- Identify collisions across instances and charts.

### WS-02 — Namespace contract

- Define deterministic IDs from canonical identity, version, instance, symbol, timeframe and event identity.
- Forbid unstable randomness and global unowned prefixes.

### WS-03 — Anchor semantics

- Freeze source candle, availability time, start/end time, price anchor and extension behavior.
- Separate fixed-timeframe and host-chart projections.

### WS-04 — Lifecycle contract

- Specify initialization, historical backfill, incremental update, restart, timeframe change, symbol change, deinitialization and owned cleanup.

## Required repository artifacts

- visual_object_inventory.json
- visual_namespace_registry.json
- visual_anchor_contracts/
- visual_lifecycle_contracts/
- multi_instance_collision_report.json
- LCM11A_TO_LCM11B_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Every active visual object has owner and source event.
- Object IDs deterministic and collision-resistant.
- Drawing is not source truth.
- Delete policy owns only its namespace.
- Unknown anchor semantics block migration.

## Hostile review

- Object name collision.
- Deletion by broad prefix.
- Non-host symbol price drawn on wrong chart.
- Current-bar drawing presented as closed-bar confirmation.
- Backfill behavior different from live incremental behavior.

The hostile review must attempt to disprove readiness. Aggregate success cannot compensate for a failed non-compensatory gate, and a low-frequency mismatch cannot be discarded merely because overall parity is high.

## Failure semantics

- `FAILED`: a required deterministic gate failed; no handoff may be issued.
- `BLOCKED`: required evidence, owner decision or tool environment is unavailable; affected scope remains unchanged.
- `UNKNOWN`: evidence does not support PASS or FAIL; UNKNOWN is blocking wherever the contract marks the dimension mandatory.
- `PARTIAL`: artifacts exist but acceptance is incomplete; PARTIAL output remains unpublished or is quarantined as diagnostic evidence.
- No failure state authorizes reconstruction of lost behavior from prose.

## Rollback requirements

- Restore the exact upstream input snapshot and verify its manifest.
- Reverse only paths listed in the patch rollback manifest.
- Restore relevant configuration, generated locator, persistent state and compatibility records, not merely source files.
- Re-run the smallest direct verification set after rollback.
- Record rollback outcome and any residual state divergence.

## Acceptance gate

- Visual inventory and contracts are frozen.
- All visualizers map to canonical events or blockers.
- Implementation work is authorized without semantic redesign.

## Handoff contract

- Object and anchor contract digests.
- Collision blockers.
- Allowed next action: implement isolation and parity.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.


## Implementation receipt — 2026-07-21

LCM-11A is implemented under `VISINV_B28F18FA1713109D58BC932384901AA4`. The frozen inventory contains 128 visual surfaces, including 84 chart-object creation sites, 36 indicator-buffer bindings and 8 report projections. It emits 128 deterministic namespace contracts, 128 anchor contracts and 128 lifecycle contracts. Canonical namespace simulation reports zero collisions across same-chart multi-instance, cross-chart, cross-timeframe and cross-event scenarios. Legacy collision risks, missing cleanup evidence and current-bar or runtime anchor uncertainty remain explicit blockers for LCM-11B; they are not waived.

The implementation is reference-only. Drawing remains a projection of canonical events, never source truth. No visualizer cutover, source move, source deletion, order path, paper path, runtime authority, promotion authority or capital authority is created.
