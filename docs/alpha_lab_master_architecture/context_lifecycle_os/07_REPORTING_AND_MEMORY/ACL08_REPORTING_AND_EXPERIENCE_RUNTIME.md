---
title: Acl08 Reporting And Experience Runtime
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-08, reporting]
---
# Acl08 Reporting And Experience Runtime

Defines the end-to-end deterministic runtime from verified ACL-07 evidence through machine reports, audience views, experience records, event ledger, provenance and ACL-09 handoff.

## Invariants

- Exact identities and digests resolve.
- UNKNOWN remains explicit.
- Diagnostic evidence remains segregated.
- Generated content is immutable and replayable.
- Promotion, order and capital authority remain false.

## Failure behavior

Any missing identity, schema mismatch, policy drift, authority escalation or integrity failure stops publication.
