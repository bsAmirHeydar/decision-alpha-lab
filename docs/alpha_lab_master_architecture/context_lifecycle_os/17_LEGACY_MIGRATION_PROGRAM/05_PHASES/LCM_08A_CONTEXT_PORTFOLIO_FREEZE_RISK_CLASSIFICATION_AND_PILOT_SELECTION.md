---
title: "LCM-08A — Context Portfolio Freeze, Risk Classification and Pilot Selection"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-08A
master_phase: LCM-08
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-08A — Context Portfolio Freeze, Risk Classification and Pilot Selection

## Purpose

Freeze the complete Context migration portfolio before any Context package is authored, assign evidence-backed risk and complexity classes, and select one pilot through a deterministic decision record rather than convenience or business preference.

## Claim ceiling

`LCM_08A_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- All legacy and partially canonical Context candidates reachable from LCM-01 through LCM-07 registries.
- Context-like logic embedded in Experts, indicators, shared includes, scripts, tests, generated packages and documentation.
- Ownership, authority, identity, locator, characterization-readiness and shared-engine dependencies.
- Wave assignment and pilot selection.

## Explicit non-goals

- No Context source move, rewrite, adapter publication, consumer switch or deletion.
- No assumption that file name, experiment number or documentation namespace equals one Context identity.
- No selection of a high-value strategy merely because it is strategically important.

## Entry contract

- LCM-07 accepted handoff and digest.
- LCM-01 source and capability survey.
- LCM-02 classification and ownership registries.
- LCM-03 identity, alias and locator registries.
- LCM-04 characterization readiness and evidence gaps.
- LCM-05 target topology.
- LCM-06 migration framework.
- LCM-07 protected-platform and shared-engine candidate registries.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Portfolio reconstruction

- Join source artifacts, documentation, aliases, callers, capabilities and known ownership into a closed Context-candidate registry.
- Represent ambiguous candidates as explicit UNKNOWN records; never force classification to reach a numerical total.
- Detect embedded Context fragments in visual, setup, treatment and execution modules.

### WS-02 — Risk and complexity model

- Score statefulness, multi-timeframe alignment, session/DST dependence, persistence, file I/O, drawing, multi-chart behavior, execution coupling, broker coupling, future-aware diagnostics, documentation completeness and testability.
- Keep raw dimensions and rationale; a total score may rank work but cannot erase a critical dimension.
- Assign risk class LOW, MODERATE, HIGH, CRITICAL or UNKNOWN.

### WS-03 — Dependency and wave assignment

- Bind each candidate to required shared engines, upstream Contexts, downstream Setups and active consumers.
- Place candidates into waves by dependency and risk, not age or perceived profitability.
- Block wave assignment when identity or ownership is unresolved.

### WS-04 — Pilot selection

- Apply deterministic eligibility rules: read-only, non-ordering, bounded state, clear known-time semantics, limited timeframe surface, owner available, evidence examples available.
- Publish selected candidate, rejected candidates and rejection reasons.
- Require independent reviewer approval and a rollback-safe pilot boundary.

## Required repository artifacts

- context_portfolio_registry.json
- context_risk_dimension_registry.json
- context_risk_assessment.csv
- context_dependency_graph.json
- context_wave_assignment.json
- pilot_candidate_evaluation.json
- pilot_selection_decision.md
- unresolved_context_queue.json
- LCM08A_TO_LCM08B_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Every Context candidate resolves to one portfolio record or explicit unresolved record.
- Risk scoring is deterministic under stable inputs.
- Critical capabilities cannot be averaged away.
- Pilot has no direct order authority and no unresolved identity collision.
- No repository source path is moved or deleted.
- Registry digests bind to LCM-07 inputs.

## Hostile review

- A Setup or visualizer mislabeled as Context.
- One Context split into accidental duplicates because of path copies.
- Several semantic variants collapsed under one experiment name.
- Future-aware diagnostic logic entering pilot eligibility.
- Order APIs hidden through wrappers or generated code.
- Owner ambiguity converted into default ownership.

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

- Portfolio is closed for the phase input snapshot.
- Every candidate has owner state, identity state, risk state, dependency state and wave state.
- Exactly one pilot is selected or the phase exits BLOCKED with documented reasons.
- No migration or cutover authority has been created.

## Handoff contract

- Exact pilot identity and source digests.
- Approved pilot scope and non-goals.
- Required characterization gaps to close in LCM-08B.
- Allowed next actions limited to pilot packet construction, canonical authoring, adapter construction and parity.
- Forbidden actions include wave-wide migration, consumer cutover, quarantine, deletion and execution activation.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
