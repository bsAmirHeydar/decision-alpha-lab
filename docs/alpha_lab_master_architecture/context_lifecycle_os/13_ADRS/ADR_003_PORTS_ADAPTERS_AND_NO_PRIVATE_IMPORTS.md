---
title: Ports, Adapters and No Private Imports
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Ports, Adapters and No Private Imports

Integrate SAED, UCEE, Strategy Factory, stores, security services and MQL5 only through public ports and conformance-tested adapters.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

Direct imports couple the lifecycle to implementation details and make migrations unsafe.

## Decision

Integrate SAED, UCEE, Strategy Factory, stores, security services and MQL5 only through public ports and conformance-tested adapters.

## Consequences

Adapters declare supported contract ranges, capabilities, failure modes, latency budgets and evidence requirements.

## Validation and rollback

A compatibility matrix and contract tests gate every adapter release.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
