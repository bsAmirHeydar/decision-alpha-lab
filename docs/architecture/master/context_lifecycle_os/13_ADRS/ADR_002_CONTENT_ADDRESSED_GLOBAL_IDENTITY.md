---
title: Content-Addressed Global Identity
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Content-Addressed Global Identity

Use stable logical IDs plus immutable content digests for every material artifact.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

Paths, branch names and display names are mutable and cannot support reproducible research or secure runtime custody.

## Decision

Use stable logical IDs plus immutable content digests for every material artifact.

## Consequences

Each artifact has a logical identity, semantic version, content digest, locator record and lineage edges. A changed payload creates a new immutable revision.

## Validation and rollback

Artifact relocation does not alter identity. Collisions, digest mismatch and unresolved locator records fail closed.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
