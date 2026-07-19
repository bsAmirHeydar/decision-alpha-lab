---
title: "LCM-09B — Setup Migration, Setup Factory Binding and Behavioral Parity"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-09B
master_phase: LCM-09
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-09B — Setup Migration, Setup Factory Binding and Behavioral Parity

## Purpose

Implement canonical Setup packages, bind them to the Setup Factory under research-only authority, and prove exact decision behavior against legacy traces.

## Claim ceiling

`LCM_09B_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Canonical Setup implementations.
- Legacy adapters where consumers cannot yet change.
- Human-defined and bounded-AI candidate exposure in reference mode.
- Setup parity and variance adjudication.

## Explicit non-goals

- No promotion authority.
- No live execution authority.
- No consumer cutover outside explicit LCM-13 plans.
- No treatment semantics moved into Setup core.

## Entry contract

- LCM-09A contract handoff.
- Canonical Context packages from LCM-08C.
- LCM-06 comparator and packet framework.
- Relevant LCM-04 traces.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Package implementation

- Implement eligibility, trigger, confirmation, invalidation, cancellation, expiry and abstention as deterministic components.
- Preserve reason codes and event ordering.

### WS-02 — Compatibility and factory binding

- Translate legacy Setup inputs/outputs to canonical records.
- Register packages in Setup Factory with promotion, runtime, order and capital authority false.

### WS-03 — Decision parity

- Compare creation, suppression, no-trade, confirmation, invalidation, cancellation, expiry and entitlement.
- Test host-chart versus fixed-timeframe variants and restart behavior.

### WS-04 — Portfolio integration

- Validate Context binding, version resolution, treatment references and duplicate Setup identity.
- Publish blocked variants rather than weakening gates.

## Required repository artifacts

- canonical_setup_packages/
- setup_adapter_registry.json
- setup_factory_registration.json
- setup_golden_cases.jsonl
- setup_golden_traces.jsonl
- setup_parity_registry.json
- setup_variance_decisions.json
- LCM09B_TO_LCM10A_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Deterministic setup decisions under replay.
- No independent Context clock.
- No order API or visual-object mutation in Setup core.
- Factory registration has zero promotion/execution authority.
- All hard mismatch resolved or blocking.

## Hostile review

- Factory default changing semantics.
- Missing no-trade records.
- Setup recomputing Context with different thresholds.
- Suppression deleting evidence.
- Expiry restored incorrectly after restart.

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

- All active Setup identities are canonical or explicitly blocked.
- Setup Factory can expose reference candidates without promotion authority.
- Treatment references are explicit and ready for LCM-10.

## Handoff contract

- Canonical Setup registry and parity digests.
- Treatment dependency inventory seed.
- Forbidden actions: order routing, capital activation, broad consumer cutover.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
