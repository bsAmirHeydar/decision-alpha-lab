---
title: ACL-11 Atomic — Training Forbidden
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-11, atomic-concept]
---
# Training Forbidden

## Definition

`Training Forbidden` is an atomic ACL-11 concept used in runtime parity assessment and non-executable custody. Its identity and semantics are explicit, versioned and independently testable.

## Invariant

It cannot upgrade its own authority, convert missing evidence to PASS, create a runtime candidate or authorize generation, signing, activation, orders or capital.

## Failure semantics

Ambiguous identity, missing evidence, invalid digest, incompatible version or unauthorized mutation fails closed with a registered reason code.

## Related

- [[ACL11_RUNTIME_PARITY_AND_CUSTODY_RUNTIME]]
- [[ACL11_PARITY_ASSESSMENT_MODEL]]
