---
title: "LCM-12 — Documentation and Obsidian Reconciliation"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-12
---
# LCM-12 — Documentation and Obsidian Reconciliation

Create one authoritative knowledge path per identity while preserving source doctrine, owner decisions, historical evidence and generated navigation.

## Claim ceiling

`KNOWLEDGE_RECONCILIATION_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-12.1 Documentation authority map

Classify every page as canonical, source evidence, implementation evidence, generated projection, superseded, duplicate, archive or unknown.

### WP-12.2 Exact duplicate consolidation

Reconcile byte-identical namespaces only after link and locator analysis. Keep redirects for externally referenced paths.

### WP-12.3 Superset reconciliation

Compare the UCEE master copy and larger standalone namespace; promote missing canonical material rather than deleting the superset.

### WP-12.4 Domain package links

Bind each Context, Setup, Treatment and visualizer to doctrine, decisions, tests and migration packet.

### WP-12.5 Generated knowledge policy

Mark source cards, atomic concepts, indexes and canvases as generated with rebuild source/digest.

### WP-12.6 Obsidian integrity

Repair links, aliases, frontmatter IDs, orphan pages and conflicting titles.

## Repository-specific target paths

- `docs/alpha_lab_master_architecture/`
- `docs/contexts/<context_id>/`
- `docs/generated/`
- `docs/archive/legacy_contexts/`

## Mandatory verification

- wiki link and alias scan
- duplicate basename/canonical ID scan
- generated marker validation
- canonical successor resolution
- open decisions retained
- no source authority deleted

## Hostile-review focus

- deleting unique content inside a near-duplicate tree
- generated page overriding doctrine
- broken external links
- two canonical pages with same identity

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Each active identity has one canonical documentation entry; all other pages have explicit source/generated/superseded/archive status and resolvable successor.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
