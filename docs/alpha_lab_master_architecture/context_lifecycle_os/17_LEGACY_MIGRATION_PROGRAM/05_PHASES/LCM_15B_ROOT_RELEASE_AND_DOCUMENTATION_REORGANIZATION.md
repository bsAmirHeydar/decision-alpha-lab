---
title: "LCM-15B — Root, Release and Documentation Reorganization"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-15B
master_phase: LCM-15
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-15B — Root, Release and Documentation Reorganization

## Purpose

Relocate root release artifacts, installers, reports and approved documentation through canonical registries while preserving historical lookup, redirects and exact provenance.

## Claim ceiling

`LCM_15B_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Root manifests, hashes, inventories, QA, commit records, installer scripts, release notes and patch references.
- Approved documentation relocation and exact duplicate redirects.

## Explicit non-goals

- No deletion.
- No rewrite of historical release evidence.
- No relocation without old/new locator and compatibility decision.

## Entry contract

- LCM-15A relocation approvals.
- LCM-12B documentation locator.
- LCM-05 target topology.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Release registry relocation

- Move release metadata into phase/version-scoped registry packages.
- Preserve original filenames as metadata and provide lookup index.

### WS-02 — Installer organization

- Move active installers/scripts to controlled tool paths; preserve historical instructions as release evidence.

### WS-03 — Documentation organization

- Apply approved canonical moves and redirect stubs.
- Keep generated and authored boundaries.

### WS-04 — Root control

- Define allowlist for files remaining at repository root.
- Produce before/after root map without deleting non-approved items.

## Required repository artifacts

- root_relocation_manifest.json
- release_registry_index.json
- installer_locator_registry.json
- documentation_relocation_receipts.json
- root_allowlist.json
- post_relocation_reference_report.json
- LCM15B_TO_LCM15C_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Every move has exact source/destination/hash.
- Historical release lookup preserved.
- Redirects resolve.
- No approved deletion executed.
- Root allowlist violations explicit.

## Hostile review

- Installer path embedded in external automation.
- Overwriting same-named release metadata.
- Moving current commit message unexpectedly.
- Redirect ambiguity.

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

- Repository structure is organized enough for exact destructive review.
- All deletion paths are revalidated against post-move topology.

## Handoff contract

- Post-relocation digest.
- Revalidated deletion ledger.
- Rollback instructions for every move.
- Allowed next action: exact controlled deletion only.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
