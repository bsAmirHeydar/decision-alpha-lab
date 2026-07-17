---
title: Security as an Independent Policy Plane
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Security as an Independent Policy Plane

Enforce security outside domain plugins through identity-aware policy decision and enforcement points.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

A plugin that can disable its own safeguards is not secure.

## Decision

Enforce security outside domain plugins through identity-aware policy decision and enforcement points.

## Consequences

The security plane controls capabilities, secrets, egress, artifact trust, signing, release, terminal access and incident actions.

## Validation and rollback

Security-denied actions produce evidence and cannot silently downgrade.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
