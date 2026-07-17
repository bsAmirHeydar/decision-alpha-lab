---
title: Dual-Lane Setup Factory with Single IR
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Dual-Lane Setup Factory with Single IR

Human-authored and AI-generated Setups compile into the same canonical Setup Policy IR.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

Separate execution paths hide behavioral duplication and create incomparable evidence.

## Decision

Human-authored and AI-generated Setups compile into the same canonical Setup Policy IR.

## Consequences

Origin remains provenance, not behavior identity. Equivalent behavior deduplicates to one Treatment identity.

## Validation and rollback

AI generation is bounded by registries, constraints, budgets and search authority.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
