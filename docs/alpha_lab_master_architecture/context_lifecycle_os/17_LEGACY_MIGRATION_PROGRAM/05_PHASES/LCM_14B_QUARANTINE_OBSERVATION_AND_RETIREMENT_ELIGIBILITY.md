---
title: "LCM-14B — Quarantine, Observation and Retirement Eligibility"
status: accepted-reference
version: 1.0.0
updated: 2026-07-22
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-14B
master_phase: LCM-14
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-14B — Quarantine, Observation and Retirement Eligibility

## Purpose

Remove approved legacy originals from active compile/runtime paths into immutable quarantine, observe for hidden references, and determine retirement eligibility without deletion.

## Claim ceiling

`LCM_14B_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Original bytes, source hashes, mapping, parity, rollback and provenance evidence.
- Runtime/build exclusion.
- Observation and restoration.

## Explicit non-goals

- No deletion.
- No quarantine of unresolved active consumer.
- No modification of quarantined bytes.

## Entry contract

- LCM-14A deprecation registry and clean reference evidence.
- Approved quarantine policy and target path.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Quarantine package

- Store original tree, manifest, hashes, successor map, parity report, rollback and owner approvals.

### WS-02 — Active-path removal

- Use exact move list; update locator and ensure quarantine excluded from compile, packaging and runtime discovery.

### WS-03 — Observation

- Run scheduled scans and capture newly discovered references.
- Reset eligibility clock when a meaningful reference is found.

### WS-04 — Restoration drill

- Restore selected packages and verify hash, compile/replay where tools exist, then return to quarantine.

### WS-05 — Eligibility

- Evaluate compatibility window, zero-reference evidence, restoration success and retained evidence.

## Required repository artifacts

- quarantine_packages/
- quarantine_registry.json
- observation_ledger.jsonl
- restoration_drill_reports/
- retirement_eligibility_registry.json
- LCM14B_TO_LCM15A_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Quarantined bytes match source hashes.
- Quarantine excluded from active paths.
- Reference scans clean for required window or blockers explicit.
- Restoration succeeds for sampled/high-risk packages.

## Hostile review

- Quarantine accidentally compiled.
- Generated build still copies source.
- Observation window shortened for convenience.
- Binary/source evidence separated.

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

- Eligible identities may enter deletion proof.
- Ineligible identities remain quarantined or compatibility-active.
- No deletion has occurred.

## Handoff contract

- Retirement eligibility decisions.
- Exact candidate paths and retained evidence locations.
- Allowed next action: deletion proof only.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.

## Implemented outcome — 2026-07-22

LCM-14B is implemented under quarantine package `QUARANTINE_F2B27A6A93EB63C1B264B84DAFA00C2D`. The phase creates 136 immutable documentation payload packages, retains all 136 compatibility redirects and canonical sources, executes two deterministic repository observation cycles per identity, records zero meaningful active repository references, and passes byte-exact restoration rehearsal for every package. External consumer evidence remains explicit UNKNOWN, so all 136 identities are eligible only to enter LCM-15A reference proof; none is deletion-approved. The 477 active-source identities remain unchanged and outside quarantine. Handoff: `sha256:beb66a4bb6792692608c4223763f7f88198e62d63a51b217436e1b456ab02cb8`.
