---
title: One-Hour Assessment Is Triage
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# One-Hour Assessment Is Triage

The one-hour Context product provides bounded evidence and next actions, never production authority.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

A short analysis can estimate support and value but cannot complete prospective validation.

## Decision

The one-hour Context product provides bounded evidence and next actions, never production authority.

## Consequences

The product reports completeness, occurrence support, constrained-random comparisons, candidate Setup families, uncertainty, failure signatures and evidence gaps.

## Validation and rollback

Claims are automatically capped at RESEARCH_TRIAGE.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
