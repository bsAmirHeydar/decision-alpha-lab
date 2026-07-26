---
title: Generated Projections Are Not Sources of Truth
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Generated Projections Are Not Sources of Truth

Machine-readable contracts and immutable evidence are authoritative; Markdown, dashboards and code mirrors are generated projections.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

Hand-edited reports and runtime mirrors drift from source evidence.

## Decision

Machine-readable contracts and immutable evidence are authoritative; Markdown, dashboards and code mirrors are generated projections.

## Consequences

Generated files contain source digests and regeneration instructions. CI rejects unauthorized edits.

## Validation and rollback

Human review comments are stored as signed decision artifacts, not modifications to generated results.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
