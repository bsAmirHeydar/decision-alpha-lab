---
title: "LCM-03 — Canonical Identity, Alias and Locator"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-03
---
# LCM-03 — Canonical Identity, Alias and Locator

Create stable domain identities independent of current paths and register every legacy name, include, function, object prefix and document slug as an alias.

## Claim ceiling

`IDENTITY_AND_LOCATOR_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-03.1 Canonical identity design

Assign versioned IDs for Contexts, Setups, Treatments, visualizers, engines and adapters. Split identities when materially different variants exist.

### WP-03.2 Legacy alias registry

Map experiment codes, old paths, public includes, function names, input names, object prefixes and documentation pages.

### WP-03.3 Artifact locator

Create identity-to-artifact resolution with version, compatibility range, authority class and canonical/legacy status.

### WP-03.4 Collision analysis

Detect aliases that resolve to multiple behaviors, case-only path conflicts, reused object prefixes and duplicate IDs.

### WP-03.5 Version policy

Record which differences require a major semantic version, compatible minor version or adapter-only patch.

### WP-03.6 Consumer census

List every known consumer of each legacy alias before redirect work begins.

## Repository-specific target paths

- `registry/legacy_context_migration/identities/`
- `registry/legacy_context_migration/aliases/`
- `registry/legacy_context_migration/locators/`

## Mandatory verification

- identity resolution is deterministic
- unknown version fails closed
- alias collision blocks resolution
- old include paths resolve only through declared compatibility rules
- object-prefix collisions are reported

## Hostile-review focus

- merging variants such as fixed-15m and host-chart close
- using filename as permanent identity
- losing old report links
- object name collisions across chart instances

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Every migration candidate resolves to one canonical identity candidate or an explicit ambiguity record; all active legacy consumers are enumerated.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
