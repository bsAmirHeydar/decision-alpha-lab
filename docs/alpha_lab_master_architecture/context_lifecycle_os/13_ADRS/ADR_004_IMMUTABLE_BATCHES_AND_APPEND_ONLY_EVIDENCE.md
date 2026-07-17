---
title: Immutable Batches and Append-Only Evidence
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Immutable Batches and Append-Only Evidence

Freeze all research inputs before execution and append evidence instead of rewriting history.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

Mutable experiment definitions make statistical exposure unknowable and invalidate auditability.

## Decision

Freeze all research inputs before execution and append evidence instead of rewriting history.

## Consequences

A Batch seals Context, data, Setup universe, models, splits, costs, budgets, seeds, code and environment. Corrections create a superseding Batch.

## Validation and rollback

Reports are projections of structured artifacts and may be regenerated without changing evidence.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
