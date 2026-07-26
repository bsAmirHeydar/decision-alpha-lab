---
title: "LCM-13A — Dual-Run Harness and Mismatch Registry"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-13A
master_phase: LCM-13
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-13A — Dual-Run Harness and Mismatch Registry

## Purpose

Build and operate a deterministic dual-run harness that executes legacy and canonical paths against the same causal inputs and records every mismatch without automatic suppression.

## Claim ceiling

`LCM_13A_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Context, Setup, Treatment-intent and visual projections that are cutover candidates.
- Historical replay, controlled live-like feed and restart scenarios.
- Mismatch taxonomy and adjudication workflow.

## Explicit non-goals

- No production consumer switch.
- No tolerance that hides categorical state or time differences.
- No deletion or quarantine.

## Entry contract

- Cutover-ready registries from LCM-08 through LCM-12.
- Golden fixtures and parity dimensions.
- Exact consumer inventory.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Harness design

- Feed identical normalized events and clocks to legacy and canonical paths.
- Isolate side effects and disable broker submission.

### WS-02 — Comparison

- Compare known-time, state, event, decision, request, visual anchor and reason-code dimensions.
- Use dimension-specific tolerances only where contractually valid.

### WS-03 — Mismatch registry

- Persist raw observations, normalized comparison, source digests, severity, owner and status.
- Never drop repeated mismatches without an approved aggregation rule.

### WS-04 — Adjudication

- Classify implementation defect, legacy defect, approved variance, fixture defect, environmental variance or UNKNOWN.
- Require evidence and reviewer approval.

## Required repository artifacts

- dual_run_harness/
- dual_run_scenario_registry.json
- mismatch_registry.jsonl
- mismatch_taxonomy.json
- variance_approval_registry.json
- dual_run_summary.md
- LCM13A_TO_LCM13B_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Harness input equality and deterministic replay.
- All hard mismatch dimensions compared.
- No unresolved HIGH/CRITICAL mismatch for cutover candidates.
- Submission remains disabled.

## Hostile review

- Different data availability between paths.
- Tolerance applied to timestamps or states.
- Mismatch aggregation hiding rare edge cases.
- Environmental failure mislabeled as parity.

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

- Dual-run evidence is sufficient to identify cutover-eligible consumers.
- Every mismatch is resolved, accepted by ADR, or blocking.

## Handoff contract

- Consumer eligibility list.
- Mismatch and variance digests.
- Exact cutover prerequisites and rollback triggers.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
