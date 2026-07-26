---
title: Acl07 Reason Code
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-07, atomic-concept]
---
# Acl07 Reason Code

## Definition

`ACL07_REASON_CODE` is an atomic concept in ACL-07. It has one semantic owner and must not be silently redefined by reporting, execution or capital layers.

## Invariant

The concept is identity-bound, replayable and governed by the ACL-07 claim ceiling. Unknown evidence remains unknown.

## Failure mode

Ambiguity, missing lineage, digest mismatch, authority escalation or diagnostic contamination fails closed.

## Related

- [[ACL07_UNIFIED_VALIDATION_RUNTIME]]
- [[ACL07_GATE_REGISTRY]]
- [[ACL07_DECISION_POLICY]]
