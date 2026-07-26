---
title: ACL-01 — Repository, Identity and Artifact Locator
status: accepted-reference-implementation
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle, acl-01]
---
# ACL-01 — Repository, Identity and Artifact Locator

ACL-01 operationalizes the canonical repository architecture defined by the ACL-OS baseline. It provides path-independent artifact identity, canonical placement, owner/schema/plugin registries, deterministic lookup, content verification, dependency direction, global lineage, compatibility resolution, migration governance and repository scanning.

## Delivered control-plane services

- `ArtifactIdentity` with semantic version and SHA-256 content binding.
- `RepositoryRegistry` with deterministic content-addressed snapshots.
- ACL-00 mutation-permit enforcement for all registry writes.
- Zone-aware path validation and generated-file provenance enforcement.
- Owner, schema and plugin registration boundaries.
- Exact, alias and version-constrained artifact resolution.
- Digest, path-confinement, symlink and status verification.
- Dependency and derivation graph validation.
- Interface, schema and security-aware compatibility resolution.
- Idempotent, dry-runnable and rollback-backed migration registration.
- Repository scanner, CLI, closed schemas, fixtures, MQL5 static mirrors and full QA.

## Claim ceiling

`REFERENCE_REPOSITORY_CONTROL_PLANE`. This phase does not prove production IAM, external object-store durability, hardware signing, live runtime parity, statistical edge, broker behavior or capital authorization.

## Handoff

Proceed to [[ACL_02_CONTEXT_STANDARD_AND_INTAKE]]. ACL-02 must consume ACL-01 identity, ownership, schema, path and locator contracts rather than creating a Context-specific alternative.
