---
title: No Direct Online Model Mutation
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# No Direct Online Model Mutation

Production observations cannot directly mutate an active model, threshold, Setup or doctrine.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

Unreviewed online adaptation breaks reproducibility, authority and rollback.

## Decision

Production observations cannot directly mutate an active model, threshold, Setup or doctrine.

## Consequences

Observations become surveillance events, experience, proposals and new Batches. Deployment requires a new promoted runtime generation.

## Validation and rollback

Emergency controls may restrict or stop behavior but cannot create new trading logic.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
