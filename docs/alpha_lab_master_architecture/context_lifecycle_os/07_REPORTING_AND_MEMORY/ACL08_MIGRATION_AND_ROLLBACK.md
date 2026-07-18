---
title: Acl08 Migration And Rollback
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-08, reporting]
---
# Acl08 Migration And Rollback

Breaking report semantics require a major version. Rollback removes the whole ACL-08 patch and regenerates outputs from ACL-07.

## Invariants

- Exact identities and digests resolve.
- UNKNOWN remains explicit.
- Diagnostic evidence remains segregated.
- Generated content is immutable and replayable.
- Promotion, order and capital authority remain false.

## Failure behavior

Any missing identity, schema mismatch, policy drift, authority escalation or integrity failure stops publication.
