---
title: ACL-15 — Migration Plan
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-15, fleet-operations, closure]
---
# Migration Plan

## Contract

This component preserves the exact ACL-14 pilot-design state and participates only in governed reference fleet registration and non-capital lifecycle closure.

## Invariants

- Pilot design is not prospective evidence.
- Unknown, failed and unexecuted states remain explicit.
- Closed history is immutable.
- Reopen requires a new permit and policy-approved evidence or migration action.
- Validation, promotion, runtime, live orders and capital remain denied.

## Verification

The direct ACL-15 suite, ACL-14 regression, digest replay, event-chain validation, schema closure, MQL5 forbidden-API scan and root-relative delivery checks cover this contract.

## Related

- [[ACL_15_FLEET_OPERATIONS_AND_CLOSURE]]
- [[ACL15_PROGRAM_CLOSURE]]
