---
title: "LCM-12A — Documentation Authority, Duplicate Analysis and Canonical Mapping"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-12A
master_phase: LCM-12
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-12A — Documentation Authority, Duplicate Analysis and Canonical Mapping

## Purpose

Classify the complete knowledge estate by authority and provenance, prove exact or semantic duplication, and map every active document to a canonical identity before relocation.

## Claim ceiling

`LCM_12A_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Doctrine, specifications, ADRs, READMEs, installers, reports, generated Obsidian projections, source cards, atomic concepts and release metadata.
- Exact duplicate trees, partial supersets and contradictory documents.
- Links from code, docs, scripts and external-facing root files.

## Explicit non-goals

- No document deletion.
- No relocation before inbound-link and successor proof.
- No generated note promoted to authority because it is more detailed.

## Entry contract

- LCM-01 documentation survey.
- LCM-02 authority classifications.
- Canonical Context/Setup/Treatment/Visualizer registries.
- Current Obsidian graph.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Authority classification

- Assign canonical, supporting evidence, generated projection, superseded, duplicate, contradictory, archive-only or unknown.
- Bind owner and version.

### WS-02 — Duplicate analysis

- Distinguish byte duplicate, normalized duplicate, partial superset and semantic overlap.
- Require exact evidence before merge or removal.

### WS-03 — Canonical mapping

- Map document to entity identity, contract version and source digest.
- Define successor and redirect requirements.

### WS-04 — Contradiction registry

- Surface conflicting doctrine or implementation statements for owner decision.
- Do not reconcile by editorial preference.

## Required repository artifacts

- documentation_authority_registry.json
- documentation_duplicate_registry.json
- documentation_canonical_map.json
- documentation_contradiction_registry.json
- documentation_inbound_reference_graph.json
- documentation_unknown_queue.json
- LCM12A_TO_LCM12B_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Every active document classified or explicitly unknown.
- Exact duplicate claims have hash proof.
- Superset claims list unique content.
- Canonical map references valid entity identities.
- No document moved or deleted.

## Hostile review

- Generated docs treated as source of truth.
- Installer history deleted as clutter.
- External links assumed absent.
- Contradictory semantics silently harmonized.

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

- Documentation authority and successor map are complete enough for controlled relocation.
- Unknowns block only affected paths and remain visible.

## Handoff contract

- Approved relocation candidates.
- Redirect requirements.
- Contradiction decisions and blockers.
- Allowed next action: Obsidian reconciliation and non-destructive moves.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
