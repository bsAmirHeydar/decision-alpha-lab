---
title: ACL-12 Atomic Concept — Tabletop Evidence
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-12, atomic-concept]
---
# Tabletop Evidence

## Definition

`TABLETOP_EVIDENCE` is an atomic ACL-12 security concept. It has one bounded meaning, one authority boundary and one deterministic representation.

## Invariant

It cannot imply production readiness, runtime activation, order authority, capital authority or production key access unless a later phase provides explicit environment-specific evidence and authorization.

## Representation

The machine representation is schema-validated, content-addressed and connected to the ACL-12 event and provenance graphs.

## Failure behavior

Missing, ambiguous, unregistered or contradictory values fail closed with a reason code.

## Related

- [[ACL12_SECURITY_CONTROL_REGISTRY]]
- [[ACL12_SECURITY_READINESS_DECISION]]
