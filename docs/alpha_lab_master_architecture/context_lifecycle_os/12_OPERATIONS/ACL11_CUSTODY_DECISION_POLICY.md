---
title: Acl11 Custody Decision Policy
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-11, runtime, custody]
---
# Acl11 Custody Decision Policy

Defines the three non-executing decision classes and exact prerequisites for any future signed build eligibility.

## Responsibility boundary

ACL-11 may verify the ACL-10 package, evaluate registered parity requirements and issue a non-executable custody decision. It may not invent a runtime candidate, alter a promotion decision, create production signatures, activate a runtime, submit orders or allocate capital.

## Invariants

- Exact source identities and digests are preserved.
- Missing or UNKNOWN evidence fails closed.
- Runtime generation requires an eligible candidate and complete parity evidence.
- Signing authority is separate from assessment authority.
- Generated output is immutable, replayable and atomically published.

## Failure behavior

Integrity mismatch, unknown schema, unregistered requirement, candidate invention, parity bypass, key injection or authority escalation stops publication with a registered reason code.

## Claim ceiling

`RUNTIME_CUSTODY_DECISION_REFERENCE_ONLY`

## Related

- [[ACL11_RUNTIME_PARITY_AND_CUSTODY_RUNTIME]]
- [[ACL11_ACL12_HANDOFF]]
- [[ADR_012_SIGNED_IMMUTABLE_RUNTIME_GENERATIONS]]
