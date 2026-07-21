---
title: "LCM-10C — Dry-Run Parity, Safety Controls and Authority-Negative Closure"
status: accepted-reference
version: 1.1.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-10C
master_phase: LCM-10
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-10C — Dry-Run Parity, Safety Controls and Authority-Negative Closure

## Purpose

Prove request-intent and lifecycle parity with submission disabled, validate safety controls, and demonstrate that migration has not created runtime, order or capital authority.

## Claim ceiling

`LCM_10C_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Dry-run and paper-simulator request lifecycle.
- Duplicate guard, stale quote, spread, volume, stop distance, session, reconciliation, kill switch and rejection behavior.
- Authority-negative test suite.

## Explicit non-goals

- No live broker connection required for PASS.
- No claim of production security or broker parity without actual evidence.
- No capital approval.

## Entry contract

- LCM-10B disabled adapters and treatment packages.
- Legacy request traces where available.
- Platform constraints and symbol fixtures.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Request parity

- Compare side, symbol, entry, stop, target, volume request, expiry, reason codes and lifecycle transitions.
- Preserve rejection and no-request outcomes.

### WS-02 — Safety control validation

- Test duplicate decisions, stale data, excessive spread, invalid tick alignment, invalid volume, stop/freeze levels, closed session, missing quote and reconciliation mismatch.

### WS-03 — Authority-negative proof

- Static scan and runtime tests must show no live submission path can be activated by default, configuration omission or research component.
- Verify Context, Setup, reports and AI layers cannot acquire adapter capability.

### WS-04 — Closure registry

- Publish treatment and execution dispositions, residual broker unknowns and conditions for future paper/shadow work.

## Required repository artifacts

- dry_run_golden_requests.jsonl
- execution_parity_report.json
- safety_control_test_report.json
- authority_negative_test_report.json
- forbidden_api_scan.json
- treatment_execution_closure.md
- LCM10C_TO_LCM11A_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Dry request parity passes for supported paths.
- All safety controls fail closed.
- Live order count and capital activation count remain zero.
- Unavailable broker evidence is UNKNOWN, not PASS.

## Hostile review

- Paper adapter calling real API.
- Configuration fallback enabling submission.
- Duplicate request after restart.
- Reconciliation state leaking across symbols.
- Claims exceeding observed evidence.

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

- Treatment portfolio and execution boundary are canonical.
- Submission remains disabled.
- Residual broker/platform unknowns are explicit.
- Visualizer work can consume canonical records without accessing broker state.

## Handoff contract

- Canonical Treatment registry.
- Disabled adapter registry.
- Authority-negative evidence.
- Forbidden actions remain live activation and capital use.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.


## Implementation closure — 2026-07-20

LCM-10C is accepted under `TREATCLOSE_3EBD9196597715D81966936D37F1DF91`. All 422 canonical Treatment packages were replayed through deterministic dry-run lifecycle, all 483 disabled adapters passed authority-negative tests, hostile safety controls failed closed, and submission, live-order and capital activation counts remained zero. Broker runtime constraints and unresolved legacy semantics remain explicit UNKNOWNs. Master phase LCM-10 is closed at reference authority only; LCM-11A may begin visual-object inventory without accessing broker state.
