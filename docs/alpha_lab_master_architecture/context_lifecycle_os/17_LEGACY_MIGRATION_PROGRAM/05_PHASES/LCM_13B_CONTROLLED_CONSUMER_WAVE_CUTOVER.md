---
title: "LCM-13B — Controlled Consumer Wave Cutover"
status: implemented-reference
version: 1.0.0
updated: 2026-07-21
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-13B
master_phase: LCM-13
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-13B — Controlled Consumer Wave Cutover

## Purpose

Switch active consumers to canonical packages in bounded waves using exact path lists, immediate health checks and automatic rollback triggers.

## Claim ceiling

`LCM_13B_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Consumers of Context, Setup, Treatment-intent, visual and documentation locators.
- Wave-specific switch manifests.
- Compatibility adapters during transition.

## Explicit non-goals

- No source deletion.
- No family-wide switch without wave evidence.
- No live order activation.

## Entry contract

- LCM-13A eligible consumer list.
- Canonical locator and adapters.
- Wave cutover plan and rollback package.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Wave plan

- Group consumers by shared dependency and blast radius.
- Define preconditions, exact files, switch mechanism, health signals, observation window and rollback trigger.

### WS-02 — Pre-cutover validation

- Clean working tree, package hashes, tests, compile where available, dual-run freshness and owner approvals.

### WS-03 — Switch

- Apply exact consumer changes in one reversible patch.
- Record legacy and canonical path resolution.

### WS-04 — Observation

- Run smoke, replay, chart, report and dry-request checks.
- Capture post-switch mismatches separately from pre-switch evidence.

## Required repository artifacts

- consumer_wave_plans/
- consumer_cutover_manifests/
- post_cutover_health_reports/
- locator_switch_receipts/
- cutover_event_ledger.jsonl
- LCM13B_TO_LCM13C_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Exact consumer list only.
- No unresolved critical mismatch.
- Health checks pass within defined window.
- Rollback package verified before switch.
- Live authority remains false.

## Hostile review

- Unlisted transitive consumer.
- Compatibility wrapper used as permanent architecture.
- Switch changes configuration defaults.
- Partial wave commit.

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

- Approved consumers resolve to canonical packages.
- Blocked consumers remain on legacy path with explicit status.
- No legacy source is removed.

## Handoff contract

- Cutover receipts and post-switch evidence.
- Rollback triggers and remaining legacy consumers.
- Allowed next action: rollback rehearsal and closure.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.

## Implemented result

LCM-13B is accepted under `CUTOVER_E38BEC955210CE172483EE47AA2D9E8C`: 613 eligible consumers are bound to canonical reference locators in 27 bounded waves, 806 blocked consumers remain on legacy, and every wave has an exact rollback package and closure handoff to LCM-13C.

## Downstream closure status

LCM-13C consumed the exact LCM-13B handoff and closed the rollback-rehearsal obligation under `CUTOVERCLOSE_0E477DA8D23F1B8DEB35DDD90B925F4F`. This does not retroactively expand LCM-13B authority.
