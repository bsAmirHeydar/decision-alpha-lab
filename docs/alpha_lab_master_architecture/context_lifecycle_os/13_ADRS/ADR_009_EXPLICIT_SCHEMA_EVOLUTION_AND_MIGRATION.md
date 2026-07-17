---
title: Explicit Schema Evolution and Migration
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Explicit Schema Evolution and Migration

All public contracts use semantic versions, compatibility declarations and executable migrations.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

Long-lived Contexts and evidence outlive individual implementations.

## Decision

All public contracts use semantic versions, compatibility declarations and executable migrations.

## Consequences

Additive changes may be minor; semantic or required-field changes are major. Migrations are idempotent, reversible where possible and tested against historical fixtures.

## Validation and rollback

Historical evidence remains interpreted under its original schema.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
