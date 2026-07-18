---
title: "LCM-01 — Forensic Repository Survey"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-01
---
# LCM-01 — Forensic Repository Survey

Convert the current repository from an opaque collection of paths into a machine-indexed evidence graph. The survey must cover all files while distinguishing metadata observations from semantic conclusions.

## Claim ceiling

`FORENSIC_SURVEY_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-01.1 Full artifact inventory

Capture path, type, size, hash, extension, top-level namespace, authored/generated likelihood, release lineage and family candidate for every file.

### WP-01.2 Source dependency scan

Parse MQL5 includes, Python imports, compile entry points, test entry points, generated-code references, configuration file references and documentation links. Preserve unresolved edges.

### WP-01.3 Capability and risk scan

Flag direct order APIs, drawing APIs, file I/O, timers, Global Variables, network APIs, external model files, chart callbacks and multi-timeframe access. These are risk indicators, not reachability proof.

### WP-01.4 Documentation namespace survey

Count and fingerprint canonical, duplicate, generated, experiment and archive namespaces. Detect exact duplicate trees and partial supersets.

### WP-01.5 Root hygiene survey

Classify all root-level manifests, hashes, QA reports, installers, commit records, binary patches and unknown artifacts without moving them.

### WP-01.6 Survey reproducibility

Package scanner version, configuration, exclusions and output digest so future phases can prove inventory change.

## Repository-specific target paths

- `lab/11_strategy_factory/migration/surveys/<survey_id>/`
- `registry/legacy_context_migration/surveys/<survey_id>/`

## Mandatory verification

- repeat survey and compare canonical digest
- verify every baseline path appears exactly once
- verify include edges preserve unresolved targets
- seed known dangerous API patterns and assert detection
- prove scanner does not classify pattern hits as live authority

## Hostile-review focus

- preprocessor aliases obscuring include edges
- dynamic registration not visible statically
- generated docs overwhelming canonical authority
- false-positive API pattern hits
- case-insensitive path collisions on Windows

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Every baseline artifact has survey metadata; MQL and Python dependency candidates are indexed; root and documentation hotspots are reported; unknowns remain explicit; zero destructive changes occurred.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
