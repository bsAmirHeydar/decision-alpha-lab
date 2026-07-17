---
title: Reference Cryptography Is Not HSM Evidence
status: accepted-reference
version: 1.0.0
phase: SAED_V4_29
tags: [saed-v4, v4-29, atomic-concept]
---

# Reference Cryptography Is Not HSM Evidence

## Atomic rule

**Reference Cryptography Is Not HSM Evidence.** The rule is evaluated as a closed binary invariant in [[V4_29_Hidden_Evaluation_Air_Gap]]. It is never inferred from a nearby field and it never grants authority beyond the research-control reference.

## Consequence

Violation invalidates the affected envelope, ledger, token, result or certificate. The only permitted fallback is `quarantine`; retry, silent repair, candidate substitution, threshold adjustment and additional protected feedback are prohibited.

## Verification

The rule is covered by at least one of: exact-schema validation, canonical-hash comparison, temporal-order validation, mutation testing, token-reuse testing, future-suffix invariance, disclosure denylist testing, append-only chain verification, authority scanning or deterministic golden replay.

## Boundary

This rule does not establish real alpha, independent custody, physical isolation, HSM enforcement, independent replication, runtime parity, broker qualification, production authorization or live execution.
