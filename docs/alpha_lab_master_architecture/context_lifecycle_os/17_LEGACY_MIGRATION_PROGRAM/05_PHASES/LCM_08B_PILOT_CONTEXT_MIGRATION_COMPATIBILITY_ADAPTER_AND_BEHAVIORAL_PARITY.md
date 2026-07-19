---
title: "LCM-08B — Pilot Context Migration, Compatibility Adapter and Behavioral Parity"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-08B
master_phase: LCM-08
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-08B — Pilot Context Migration, Compatibility Adapter and Behavioral Parity

## Purpose

Migrate one approved low-risk Context end to end, prove the canonical package and compatibility path against legacy behavior, and establish the repeatable Context migration pattern without switching active consumers.

## Claim ceiling

`LCM_08B_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- One LCM-08A-selected Context identity and its closed legacy evidence set.
- Canonical ACL-compatible Context package.
- Legacy-to-canonical adapter.
- Golden occurrence, state, reference, reason-code and known-time parity.
- Pilot migration packet and reusable runbook.

## Explicit non-goals

- No active consumer cutover.
- No generalized family-wide refactor.
- No correction of legacy defects unless an approved ADR creates a separately versioned corrected behavior.
- No Setup, Treatment, drawing or execution authority inside Context core.

## Entry contract

- LCM-08A handoff.
- Selected source bytes and hashes.
- Relevant LCM-04 golden traces and characterization gaps.
- Target path from LCM-05.
- Interface, packet, comparator and rollback contracts from LCM-06.
- Approved shared-engine dependencies from LCM-07.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Evidence packet

- Capture source paths, hashes, includes, call graph, inputs, state variables, timestamps, examples, documentation and active consumers.
- Distinguish observed behavior, intended doctrine, known defects and unknowns.
- Freeze the pilot input corpus and replay clock.

### WS-02 — Semantic decomposition

- Separate data access, causal clock, state machine, occurrence generation, reference lifecycle, missingness and reason codes from Setup, visual and execution concerns.
- Document every extracted boundary and residual legacy coupling.

### WS-03 — Canonical package authoring

- Create manifest, owners, doctrine, glossary, scope, ontology, causal clock, data contract, state machine, occurrence contract, reference contract, missingness, invalidation, security and claim ceiling.
- Bind every contract to versioned identity and source evidence.

### WS-04 — Implementation and adapter

- Implement the Context core in the approved target path.
- Construct a compatibility adapter that translates legacy inputs and emits canonical observations without adding domain rules.
- Keep active consumers on legacy path during this subphase.

### WS-05 — Parity and variance adjudication

- Run deterministic replay for normal, negative, boundary, restart, duplicate-event, missing-bar, timeframe and session cases.
- Compare event ordering, state transitions, occurrence fields, references, no-observation results and reason codes.
- Classify mismatch as implementation defect, legacy defect, approved semantic amendment, fixture defect or UNKNOWN.

### WS-06 — Pilot runbook

- Record build, verify, replay, rollback and evidence-refresh procedures.
- Extract only process lessons; do not generalize domain semantics from the pilot.

## Required repository artifacts

- pilot_context_migration_packet/
- canonical_context_package/
- legacy_adapter_contract.json
- golden_cases.jsonl
- golden_event_traces.jsonl
- parity_report.json
- variance_decision_registry.json
- pilot_context_model_card.md
- pilot_rollback.md
- LCM08B_TO_LCM08C_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Canonical package schema and ACL onboarding validation.
- Known-time and closed-bar tests.
- State-transition invariant tests.
- Golden replay determinism.
- Adapter does not call order or drawing APIs.
- No active consumer path changed.
- Rollback restores exact pre-pilot state.

## Hostile review

- Current-bar or future data substitution.
- Adapter silently normalizing an intentional legacy variance.
- Drawing timing used as source truth.
- Context package absorbing trigger or treatment fields.
- Reason-code collapse that hides no-trade or missingness.
- Reference consumption/reset changes after restart.

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

- Pilot package is complete and canonical.
- Hard parity dimensions pass or have approved versioned variance decisions.
- Any UNKNOWN remains blocking for affected behavior.
- No active consumer cutover occurred.
- Reusable Context migration runbook is accepted.

## Handoff contract

- Pilot package digest and parity digest.
- Accepted variance decisions.
- Wave eligibility rules proven by pilot.
- Explicit list of reusable framework improvements and prohibited domain generalizations.
- Allowed next action is wave package migration only.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
