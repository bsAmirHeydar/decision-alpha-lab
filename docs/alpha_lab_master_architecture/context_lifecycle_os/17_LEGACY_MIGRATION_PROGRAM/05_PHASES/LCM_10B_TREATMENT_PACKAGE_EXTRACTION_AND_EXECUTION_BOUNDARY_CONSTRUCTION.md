---
title: "LCM-10B — Treatment Package Extraction and Execution Boundary Construction"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-10B
master_phase: LCM-10
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-10B — Treatment Package Extraction and Execution Boundary Construction

## Purpose

Build versioned Treatment packages and a normalized execution-intent boundary while placing broker APIs behind disabled, capability-gated adapters.

## Claim ceiling

`LCM_10B_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Treatment package contracts and implementations.
- Normalized request intent.
- MQL5 and other platform adapter interfaces.
- Compatibility wrappers with submission disabled.

## Explicit non-goals

- No live or paper submission.
- No risk policy invention.
- No Context or Setup re-evaluation inside router.
- No consumer cutover outside bounded test harnesses.

## Entry contract

- LCM-10A inventory and authority map.
- Canonical Setup treatment bindings.
- ACL runtime/security contracts.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Treatment packages

- Implement entry, stop, target, cancellation, expiry and management atoms with explicit versioning.
- Keep risk sizing separate when it is portfolio/capital policy rather than treatment semantics.

### WS-02 — Normalized request intent

- Define identity, side, symbol, decision time, availability time, entry, stop, targets, volume request, expiry, source evidence and rejection reasons.
- Represent unsupported or missing fields explicitly.

### WS-03 — Execution adapter boundary

- Place all broker APIs behind capability checks and compile-time/runtime denial defaults.
- Prevent adapters from recomputing Context or Setup.

### WS-04 — Compatibility containment

- Forward legacy consumers into normalized intent in dry mode.
- Record exact translation and any untranslatable fields.

## Required repository artifacts

- canonical_treatment_packages/
- execution_intent_schema.json
- execution_adapter_contracts/
- capability_guard_policy.json
- legacy_execution_adapter_registry.json
- forbidden_api_boundary_report.json
- LCM10B_TO_LCM10C_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Forbidden broker APIs absent outside approved adapter paths.
- Treatment outputs deterministic.
- Side-aware price and stop semantics preserved.
- Submission capability defaults false.
- Untranslatable legacy behavior blocks affected path.

## Hostile review

- Router adding filters.
- Stop/target units mixed.
- Implicit market order on missing limit.
- Adapter mode defaulting to live.
- Portfolio risk policy smuggled into Treatment.

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

- All active Treatment identities have canonical package or blocker.
- Execution intent boundary is versioned.
- Broker adapters are present only in disabled/reference form.

## Handoff contract

- Treatment and intent digests.
- Boundary scan results.
- Allowed next action: dry-run/paper simulation and authority-negative tests only.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
