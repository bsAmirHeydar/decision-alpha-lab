---
title: Late Data Policy
status: accepted-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, acl-02, atomic-concept]
---
# Late Data Policy

## Definition

**Late Data Policy** is a bounded ACL-02 concept used to make Context intake deterministic, inspectable, secure and evolvable. Its value is carried in closed machine contracts and referenced by stable artifact identity rather than by file location or informal interpretation.

## Invariants

- It cannot grant Context compiler, model, order or capital authority.
- It preserves known-time and explicit UNKNOWN semantics.
- It has an accountable owner, version, schema and evidence lineage.
- Breaking meaning requires semantic versioning, migration and rollback.
- Failure produces a registered reason code; permissive defaults are forbidden.

## Security

The concept is classified with the Context package, is denied undeclared plugin capabilities, and is excluded from inline secret storage and uncontrolled network egress.

## Verification

Schema, unit, mutation, negative-security and clean-checkout tests cover the concept according to its risk.

## Related

- [[ACL_02_CONTEXT_STANDARD_AND_INTAKE]]
- [[CONTEXT_PACKAGE_STANDARD]]
- [[CONTEXT_READINESS_REPORT]]
