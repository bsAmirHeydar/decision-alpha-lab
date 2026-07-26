---
title: Acl08 Closed Report Block Registry
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-08, reporting]
---
# Acl08 Closed Report Block Registry

Defines thirteen required report blocks and rejects dynamic or unregistered sections that could hide semantics or add authority.

## Invariants

- Exact identities and digests resolve.
- UNKNOWN remains explicit.
- Diagnostic evidence remains segregated.
- Generated content is immutable and replayable.
- Promotion, order and capital authority remain false.

## Failure behavior

Any missing identity, schema mismatch, policy drift, authority escalation or integrity failure stops publication.
