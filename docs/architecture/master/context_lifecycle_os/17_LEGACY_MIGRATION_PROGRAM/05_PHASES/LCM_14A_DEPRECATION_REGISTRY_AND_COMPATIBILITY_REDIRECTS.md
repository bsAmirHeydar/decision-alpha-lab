---
title: "LCM-14A — Deprecation Registry and Compatibility Redirects"
status: implemented-reference
version: 1.1.0
updated: 2026-07-21
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-14A
master_phase: LCM-14
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-14A — Deprecation Registry and Compatibility Redirects

## Purpose

Mark successfully replaced legacy identities as deprecated and install minimal, time-bounded redirects where active consumers still require compatibility.

## Claim ceiling

`LCM_14A_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Legacy source, include/import paths, document paths, configuration keys and entry points with canonical successors.
- Warning and compatibility policy.

## Explicit non-goals

- No original deletion.
- No wrapper may contain new domain behavior.
- No redirect for unresolved or parity-failed identity.

## Entry contract

- LCM-13C closed cutover waves.
- Canonical locator and successor registry.
- External consumer evidence.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Deprecation registry

- Record legacy identity/path, successor, start, owner, warning, compatibility window and removal gates.

### WS-02 — Redirect design

- Use the thinnest forwarding include/import/doc stub possible.
- Pin exact canonical identity/version.

### WS-03 — Active reference scan

- Scan code, configs, presets, tests, docs, generated packages and known external integration points.

### WS-04 — Warning verification

- Ensure consumers receive actionable migration guidance without altering behavior.

## Required repository artifacts

- deprecation_registry.json
- compatibility_redirect_registry.json
- active_reference_scan.json
- compatibility_warning_catalog.json
- redirect_test_report.json
- LCM14A_TO_LCM14B_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Only parity-approved successors can deprecate legacy paths.
- Redirects contain no domain logic.
- Version resolution exact.
- Original bytes remain present.

## Hostile review

- Redirect points to floating latest.
- Wrapper becomes shared implementation.
- Unknown external consumer ignored.
- Warning emitted too late to diagnose path.

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

- Deprecated identities and redirects are explicit and tested.
- Quarantine candidates have no required direct runtime use.

## Handoff contract

- Deprecation and reference digests.
- Minimum observation requirements.
- Allowed next action: quarantine copy/move and restoration drill.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.


## Implementation closure

LCM-14A is accepted under `DEPRECATION_B53138FCCDFD91CC595A818BD7153132` at claim ceiling `LCM_14A_REFERENCE_ONLY`. The package:

- accounts for all 613 LCM-13C deprecation candidates: 1 Context, 136 Documentation, 422 Treatment and 54 Visual identities;
- verifies 136 existing documentation redirect stubs and registers 477 reference-only redirects without modifying production bindings;
- pins every redirect to an exact canonical content digest and rejects floating resolution;
- resolves duplicate legacy locators only with an explicit consumer identity and fails closed for ambiguous unscoped calls;
- freezes 613 actionable warnings before resolution;
- records 12,431 active-reference records from 44,243 scanned files and 288,354,103 scanned bytes;
- marks 136 documentation identities as observation candidates while blocking 477 active-source identities from quarantine;
- records external consumer scope as UNKNOWN for all 613 identities rather than inferring absence;
- preserves original byte locations and content digests; and
- creates no quarantine, deletion, runtime, live-order or capital authority.

The bounded handoff to LCM-14B is `sha256:e6cdd8272af462e3dbf29a148343e6921cadf8c7b6f748c5ce0a0f0d50e8b3f1`. LCM-14 remains open.
