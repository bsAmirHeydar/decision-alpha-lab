---
title: "LCM-12B — Obsidian Reconciliation, Relocation and Documentation Closure"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-12B
master_phase: LCM-12
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-12B — Obsidian Reconciliation, Relocation and Documentation Closure

## Purpose

Reorganize the knowledge graph into canonical authored and generated boundaries, preserve link compatibility, and prove that the vault remains navigable and self-sufficient.

## Claim ceiling

`LCM_12B_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Canonical document moves and updates.
- Generated/source-card/atomic-concept boundaries.
- Redirect stubs.
- Obsidian links, headings, embeds, attachments and MOCs.

## Explicit non-goals

- No deletion of legacy documents; deletion remains LCM-15C.
- No semantic rewrite beyond approved contradiction decisions.
- No source code movement.

## Entry contract

- LCM-12A canonical map and relocation approvals.
- Target documentation topology from LCM-05.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Canonical relocation

- Move documents with explicit old/new locator entries and preserve Git history where possible.
- Keep release evidence under release/registry topology.

### WS-02 — Link compatibility

- Update internal links and create minimal redirect stubs for approved compatibility windows.
- Validate basename collisions and heading anchors.

### WS-03 — Authored/generated separation

- Mark generated projections and prevent edits from becoming authoritative.
- Bind generated docs to producer and source digest.

### WS-04 — Vault QA

- Validate frontmatter, MOCs, wiki links, Markdown links, attachments, orphan policies and navigation entry points.

### WS-05 — Closure

- Publish canonical knowledge registry and residual contradiction/unknown list.

## Required repository artifacts

- documentation_move_manifest.json
- documentation_redirect_registry.json
- obsidian_link_report.json
- obsidian_orphan_report.json
- generated_document_registry.json
- documentation_closure_report.md
- LCM12B_TO_LCM13A_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- All moved paths resolve through canonical locator.
- Changed-doc link validation passes.
- No canonical basename collision.
- Generated documents identify source and producer.
- No deletion occurred.

## Hostile review

- Redirect loops.
- Broken heading links.
- Two canonical notes with same ambiguous basename.
- Root installer documentation detached from release evidence.

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

- Canonical knowledge graph is navigable and version-bound.
- Legacy docs are either redirected, active compatibility, archive candidates or blockers.

## Handoff contract

- Documentation registry digest.
- Cutover-facing consumer documentation.
- Allowed next action: dual-run harness and consumer mismatch collection.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
