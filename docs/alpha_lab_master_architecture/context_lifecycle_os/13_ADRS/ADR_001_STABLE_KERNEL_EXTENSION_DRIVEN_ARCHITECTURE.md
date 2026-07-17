---
title: Stable Kernel and Extension-Driven Architecture
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Stable Kernel and Extension-Driven Architecture

Adopt a small, versioned control-plane kernel and require all Context, Setup, model, report and runtime variability to enter through registered extensions.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

A continuously evolving research system cannot freeze domain behavior into a monolith. Kernel changes have fleet-wide blast radius and therefore require a higher evidence threshold than extension changes.

## Decision

Adopt a small, versioned control-plane kernel and require all Context, Setup, model, report and runtime variability to enter through registered extensions.

## Consequences

The kernel owns identity, lifecycle transitions, policy enforcement, artifact resolution, event recording and capability isolation. Domain behavior remains outside it. Private imports across extension boundaries are forbidden.

## Validation and rollback

New functionality normally becomes an extension. Kernel modification is accepted only when no existing public contract can represent the capability without violating invariants.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
