---
title: Acl08 Input Evidence Gateway
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-08, reporting]
---
# Acl08 Input Evidence Gateway

Requires the complete ACL-07 generated root, verifies marker, manifest, receipt, embedded digests, event chain, provenance, candidate decisions and all gate vectors before reporting begins.

## Invariants

- Exact identities and digests resolve.
- UNKNOWN remains explicit.
- Diagnostic evidence remains segregated.
- Generated content is immutable and replayable.
- Promotion, order and capital authority remain false.

## Failure behavior

Any missing identity, schema mismatch, policy drift, authority escalation or integrity failure stops publication.
