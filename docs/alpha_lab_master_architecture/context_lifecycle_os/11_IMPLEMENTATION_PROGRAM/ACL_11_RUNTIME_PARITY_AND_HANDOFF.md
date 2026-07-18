---
title: ACL-11 — Runtime Parity and Handoff
status: accepted-reference-implementation
version: 3.0.0
updated: 2026-07-18
tags: [acl-os, acl-11, runtime, custody]
---
# ACL-11 — Runtime Parity and Handoff

ACL-11 consumes `ACL10_TO_ACL11`, verifies the entire promotion-state package, evaluates a closed runtime-parity prerequisite registry and publishes a non-executable custody decision. The reference upstream contains zero runtime candidates, so the only correct result is an empty generation manifest and a fail-closed handoff to ACL-12.

## Implemented vertical slice

1. ACL-10 manifest, receipt, handoff, event and provenance verification.
2. Assessment-only authority permit bound to the exact ACL-10 handoff digest.
3. Twenty registered runtime parity and custody prerequisites.
4. Explicit SATISFIED, UNSATISFIED, UNKNOWN and NOT_APPLICABLE semantics.
5. Empty immutable runtime generation manifest.
6. Signing custody plan with no key material and no signature creation.
7. Empty conformance matrix without invented MQL5 or broker evidence.
8. Non-executable runtime custody decision.
9. Trusted-computing-base declaration and capability denial report.
10. Hash-linked events, provenance, atomic publication and `ACL11_TO_ACL12`.

## Reference result

- Runtime candidates: 0
- Runtime generations: 0
- Custody decision: `NON_EXECUTABLE_NO_RUNTIME_CANDIDATES`
- Runtime activation: denied
- Live orders: denied
- Capital: denied

## Required ACL-12 behavior

ACL-12 must harden security boundaries around this non-executable package. It may not create a runtime candidate, bypass parity/signing controls, access production keys in reference mode, authorize live orders or activate capital.

## Claim ceiling

`RUNTIME_CUSTODY_DECISION_REFERENCE_ONLY`
