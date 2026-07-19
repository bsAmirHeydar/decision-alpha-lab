---
title: "LCM-15A — Deletion Candidate Inventory and Reference Proof"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-15A
master_phase: LCM-15
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-15A — Deletion Candidate Inventory and Reference Proof

## Purpose

Construct the only authoritative deletion-candidate ledger and prove successor/archive coverage, zero active references, parity, approvals, quarantine maturity and recovery evidence for each path.

## Claim ceiling

`LCM_15A_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Quarantined source candidates.
- Exact duplicate documentation candidates.
- Root metadata relocation candidates.
- Obsolete compatibility wrappers whose window ended.

## Explicit non-goals

- No deletion or relocation.
- No wildcard candidate groups without exact path expansion.
- No evidence loss.

## Entry contract

- LCM-14B eligibility registry.
- LCM-12 documentation map.
- LCM-05 root relocation plan.
- Full reference scanners.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Candidate ledger

- One record per exact path and hash with category, successor/archive, owner and rationale.

### WS-02 — Reference proof

- Scan code, configs, build files, tests, docs, presets, release scripts and generated assets.
- Record unresolved external reachability as UNKNOWN.

### WS-03 — Recovery proof

- Verify archive path, hash, restore instructions and required toolchain.

### WS-04 — Approval gate

- Require domain owner, migration reviewer and deletion authority separation.

## Required repository artifacts

- deletion_candidate_ledger.json
- zero_reference_evidence/
- successor_archive_proof.json
- recovery_proof.json
- deletion_approval_registry.json
- deletion_blocker_registry.json
- LCM15A_TO_LCM15B_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Every candidate exact path/hash.
- All non-compensatory gates individually true.
- UNKNOWN cannot be approved.
- No file changed except documentation/registry artifacts.

## Hostile review

- Directory-level approval hiding unreviewed files.
- External consumer assumed absent.
- Archive exists but cannot restore.
- Duplicate classification based on title.

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

- Deletion-approved and deletion-blocked sets are closed and immutable for the snapshot.
- Reorganization may proceed only for non-destructive relocation candidates.

## Handoff contract

- Approved relocation list.
- Approved future deletion list, still not executed.
- Forbidden action: deleting during LCM-15B.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
