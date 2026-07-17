---
title: Fail-Closed Lifecycle Gates
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Fail-Closed Lifecycle Gates

Every lifecycle transition requires a closed-schema decision with evidence references and explicit reason codes.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

Implicit state inferred from files or successful commands creates unauthorized progression.

## Decision

Every lifecycle transition requires a closed-schema decision with evidence references and explicit reason codes.

## Consequences

Unknown, missing, stale, incompatible or unverifiable inputs deny progression. Waivers are separate, bounded and expiring artifacts.

## Validation and rollback

No component may promote its own output beyond its authority ceiling.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
