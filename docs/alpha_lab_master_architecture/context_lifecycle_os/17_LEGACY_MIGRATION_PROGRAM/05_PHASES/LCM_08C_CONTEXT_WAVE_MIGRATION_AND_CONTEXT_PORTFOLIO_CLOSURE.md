---
title: "LCM-08C — Context Wave Migration and Context Portfolio Closure"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-08C
master_phase: LCM-08
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-08C — Context Wave Migration and Context Portfolio Closure

## Purpose

Apply the proven pilot pattern to the remaining Context portfolio in dependency-ordered waves, producing cutover-ready canonical Context packages while preserving per-Context evidence and avoiding a family-wide rewrite.

## Claim ceiling

`LCM_08C_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- All LCM-08A portfolio entries not closed by the pilot.
- Wave-specific migration packets and canonical Context packages.
- Per-Context adapters and parity evidence.
- Context registry closure for active, archived, blocked and unresolved identities.

## Explicit non-goals

- No Setup migration beyond Context-boundary stubs.
- No active consumer cutover; consumer switching remains LCM-13.
- No deletion or quarantine.
- No shared-engine extraction without LCM-07-equivalent evidence and review.

## Entry contract

- LCM-08B accepted pilot pattern and handoff.
- Frozen wave assignment from LCM-08A, amended only through ADR.
- Per-family doctrine and owner decisions.
- Approved shared-engine contracts.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Wave admission

- Revalidate owner, identity, source reachability, evidence completeness and dependency readiness at wave start.
- Split a wave when one critical Context would hold unrelated low-risk Contexts hostage.

### WS-02 — Per-Context packet execution

- Run evidence capture, semantic decomposition, canonical authoring, adapter construction and parity independently for every Context.
- Maintain one state machine and one decision ledger per identity.

### WS-03 — Family variance control

- Preserve host-timeframe/fixed-timeframe, continuation/reversal, session, symbol, direction and reference-policy variants as explicit contracts.
- Merge only after behavioral equivalence proof.

### WS-04 — Wave integration

- Verify shared dependencies, canonical locator, duplicate identity, package boundary and cross-Context reference semantics.
- Run wave-level regression without allowing aggregate success to compensate for one failed Context.

### WS-05 — Portfolio closure

- Publish final disposition: MIGRATED_CUTOVER_READY, BLOCKED, ARCHIVE_REFERENCE_ONLY, QUARANTINE_UNCERTAIN or OUT_OF_SCOPE.
- Carry unresolved items to an explicit blocker register.

## Required repository artifacts

- wave_admission_receipts/
- context_migration_packets/
- context_package_registry.json
- context_parity_registry.json
- context_variance_registry.json
- context_blocker_registry.json
- context_portfolio_closure_report.md
- LCM08C_TO_LCM09A_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Every active Context identity has a canonical package or explicit blocking disposition.
- No hard parity dimension is failed or unknown for a CUTOVER_READY Context.
- Canonical locator is collision-free.
- Context core contains no order or visual-object authority.
- Wave regression is non-compensatory.

## Hostile review

- Family-wide search-and-replace.
- Copying the pilot semantic design into unrelated Contexts.
- Suppressing low-frequency mismatch as noise.
- Cross-symbol reference leakage.
- Session/DST engine drift.
- A blocked Context omitted from closure totals.

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

- Context portfolio registry is complete.
- All migrated packages are cutover-ready but not yet switched.
- Blocked and archived identities remain traceable.
- LCM-09 receives canonical Context interfaces and exact dependency bindings.

## Handoff contract

- Canonical Context registry digest.
- Per-Context package and parity digests.
- Blocked identity list and reasons.
- Allowed next action limited to Setup inventory and migration against canonical Context contracts.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
