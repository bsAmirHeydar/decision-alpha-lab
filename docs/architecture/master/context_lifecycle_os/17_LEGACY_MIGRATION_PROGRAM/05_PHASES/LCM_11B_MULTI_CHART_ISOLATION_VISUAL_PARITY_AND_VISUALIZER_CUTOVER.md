---
title: "LCM-11B — Multi-Chart Isolation, Visual Parity and Visualizer Cutover"
status: implemented-reference
version: 1.1.0
updated: 2026-07-21
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-11B
master_phase: LCM-11
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-11B — Multi-Chart Isolation, Visual Parity and Visualizer Cutover

## Purpose

Implement canonical visualizers, prove multi-chart and multi-instance isolation, and switch visual consumers only after anchor and lifecycle parity.

## Claim ceiling

`LCM_11B_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Canonical visualizer implementations.
- Legacy-compatible projection adapters.
- Multi-chart, multi-symbol, restart and historical backfill tests.
- Visual consumer cutover.

## Explicit non-goals

- No Context or Setup behavior change.
- No order capability.
- No deletion of legacy source.

## Entry contract

- LCM-11A contracts.
- Canonical event records.
- Golden visual fixtures and chart scenarios.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Implementation

- Render only canonical event records.
- Keep style parameters separate from event semantics.

### WS-02 — Isolation

- Use chart/instance-scoped registries, deterministic prefixes and owned cleanup.
- Test two charts, same symbol, different timeframe, and multiple instances.

### WS-03 — Visual parity

- Compare object existence, type, anchor time, anchor price, line end, label meaning, update and deletion.
- Classify style-only differences separately from semantic differences.

### WS-04 — Cutover

- Switch visual consumers under explicit path list.
- Retain compatibility projection or rollback path.

## Required repository artifacts

- canonical_visualizers/
- visual_parity_report.json
- multi_chart_test_report.json
- restart_backfill_test_report.json
- visual_cutover_manifest.json
- visual_rollback.md
- LCM11B_TO_LCM12A_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Anchor parity passes.
- No collision across tested chart scenarios.
- History reload and restart are deterministic.
- Canonical visualizer cannot mutate domain state.
- Cutover path list exact and reversible.

## Hostile review

- Visual parity judged only by screenshot appearance.
- Hidden domain calculation retained in renderer.
- Chart event recursion.
- Cleanup removes another instance objects.

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

- Active visual consumers use canonical event projections or are explicitly blocked.
- Legacy visual paths remain recoverable for LCM-14.

## Handoff contract

- Visualizer registry and cutover digest.
- Residual platform visual unknowns.
- Documentation receives canonical visual references.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.


## Implementation receipt — 2026-07-21

LCM-11B is implemented under `VISMIG_0938A2A7868358466B7B877BD1E5251D`. The phase creates 128 canonical visualizer contracts, 128 style profiles, 128 contract-golden fixtures, 128 compatibility adapter records, 512 multi-chart isolation scenarios and 768 lifecycle/restart scenarios. Fifty-four surfaces are eligible for reference-harness cutover and seventy-four remain explicitly blocked because legacy backfill or source-event semantics are not evidenced. Canonical isolation reports zero collisions and semantic parity reports zero mismatches for the eligible set.

The cutover is deliberately reference-harness-only. No production visual source is modified or deleted, no domain state may be mutated by a renderer, and no runtime, order or capital authority is created. Residual MetaEditor, live-chart restart and screenshot evidence remains UNKNOWN and is handed forward without waiver.
