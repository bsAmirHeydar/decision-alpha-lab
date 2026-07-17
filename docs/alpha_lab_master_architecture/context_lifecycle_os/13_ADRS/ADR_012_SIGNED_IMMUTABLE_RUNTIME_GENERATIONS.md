---
title: Signed Immutable Runtime Generations
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Signed Immutable Runtime Generations

Production executes only exact, signed, content-addressed runtime generations.

## Status

Accepted as the reference architecture decision. Production adoption requires implementation evidence.

## Context

Mutable terminal inputs and ad-hoc model files make parity and incident response impossible.

## Decision

Production executes only exact, signed, content-addressed runtime generations.

## Consequences

A generation binds detector, preprocessing, model, calibration, policy, Treatment, economics, risk, fallback, monitoring and rollback metadata.

## Validation and rollback

Terminals verify trust, compatibility and revocation before activation.

## Security impact

Threat-model changes, privilege changes and trust-boundary changes must be reviewed with the ADR. A superseding ADR is required to relax a control.

## Migration rule

Existing components move through an explicit compatibility adapter or migration. Big-bang replacement is prohibited unless rollback and evidence preservation are demonstrated.

## Related

- [[ACL_OS_HOME]]
- [[CHANGE_MANAGEMENT_AND_RELEASES]]
