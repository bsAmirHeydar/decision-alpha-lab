---
title: ACL-01 — Deprecation and Removal
status: accepted-reference-implementation
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, acl-01, repository, identity, lineage]
---
# ACL-01 — Deprecation and Removal

## Purpose

Defines deprecation windows, replacement references, tombstones and permanent lineage.

## Contract

ACL-01 treats identity, location, ownership, schema, compatibility and lineage as separate versioned concerns. Every mutation requires an ACL-00 permit; every resolution is read-only, content-verified and fail-closed. Unknown fields, owners, schemas, kinds, zones, endpoints or versions are not inferred.

## Invariants

- Artifact IDs are path-independent and immutable.
- Canonical paths are repository-relative, traversal-free and zone-classified.
- Generated artifacts carry complete source and generator provenance.
- Registry snapshots are deterministic and content-addressed.
- Hard dependency and derivation graphs are cycle-free.
- Cross-tenant and private implementation coupling are denied by default.
- Live-order submission and capital activation remain hard false.

## Verification

Unit, contract, property-style parameterization, graph mutation, integrity drift, path escape, alias poisoning, schema closure, MQL5 static boundary and clean-checkout delivery checks cover this contract.

## Evolution

Additive kinds, zones, interfaces and schemas use compatible minor versions. Breaking semantics require a major version, impact analysis, registered migration, rollback, dual-read where required, deprecation evidence and an ACL-00 authority decision.

## Related

- [[00_ACL_OS_HOME]]
- [[ACL_01_REPOSITORY_IDENTITY_AND_LOCATOR]]
- [[ACL_00_STATUS]]
- [[ACL_01_STATUS]]
