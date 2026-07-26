---
title: Acl08 Experience Capture Contract
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-08, reporting]
---
# Acl08 Experience Capture Contract

Creates mechanical, non-promotional experience records from decisions and gate states. Records remain not ingested until ACL-09.

## Invariants

- Exact identities and digests resolve.
- UNKNOWN remains explicit.
- Diagnostic evidence remains segregated.
- Generated content is immutable and replayable.
- Promotion, order and capital authority remain false.

## Failure behavior

Any missing identity, schema mismatch, policy drift, authority escalation or integrity failure stops publication.
