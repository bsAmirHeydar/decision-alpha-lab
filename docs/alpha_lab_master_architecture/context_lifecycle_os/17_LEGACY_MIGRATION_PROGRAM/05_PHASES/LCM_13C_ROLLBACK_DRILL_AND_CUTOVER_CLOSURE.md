---
title: "LCM-13C — Rollback Drill and Cutover Closure"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-13C
master_phase: LCM-13
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-13C — Rollback Drill and Cutover Closure

## Purpose

Prove that each consumer wave can be restored to its exact prior state and close cutover only after forward and reverse paths are verified.

## Claim ceiling

`LCM_13C_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Representative and high-risk consumer rollback rehearsals.
- Locator restoration.
- State, cache, object and file-ledger recovery.
- Cutover closure ledger.

## Explicit non-goals

- No quarantine or deletion.
- No assumption that Git revert alone restores runtime state.

## Entry contract

- LCM-13B cutover receipts.
- Pre-cutover manifests and rollback packages.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Rollback rehearsal

- Restore source/config locator and relevant state artifacts.
- Verify legacy path compile/replay and compare baseline digest.

### WS-02 — Forward recovery

- Reapply canonical switch after successful rollback and verify deterministic result.

### WS-03 — State recovery

- Check persistent files, global variables, chart objects, caches and generated registries for reversible ownership.

### WS-04 — Closure

- Classify each wave CLOSED, CLOSED_WITH_RESIDUAL_RISK or REOPEN_REQUIRED.

## Required repository artifacts

- rollback_rehearsal_reports/
- forward_recovery_reports/
- state_recovery_registry.json
- cutover_closure_registry.json
- residual_cutover_risk.md
- LCM13C_TO_LCM14A_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Rollback restores exact path and expected behavior.
- Forward reapplication is deterministic.
- Persistent state ownership verified.
- Any failed wave is reopened.

## Hostile review

- Rollback only tested on files.
- Legacy code no longer compiles because wrapper changed.
- Persistent entitlement duplicated.
- Visual objects survive under wrong owner.

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

- All closed waves have verified reversible cutover.
- Remaining legacy consumers are explicit blockers.

## Handoff contract

- Cutover closure digest.
- Deprecation candidates and required compatibility windows.
- No deletion authority.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
