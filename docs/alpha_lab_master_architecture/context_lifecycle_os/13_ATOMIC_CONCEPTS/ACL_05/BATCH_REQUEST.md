---
title: Batch Request
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-05, atomic-concept]
---
# Batch Request

## Definition

Authorized declarative request naming all material contracts and frozen time.

## Invariant

The concept is versioned, explicit and subordinate to the ACL authority hierarchy. Unknown or ambiguous values do not receive a permissive interpretation. When identity-bearing, the value is canonicalized and bound by SHA-256.

## Boundary

This concept does not independently prove alpha, data quality, production readiness, broker parity, order authority or capital permission. It may only be consumed through the contract that owns it.

## Failure semantics

Missing identity, schema drift, unresolved reference, known-time violation, mutation, capability escalation or digest mismatch fails closed with a stable ACL-05 reason code.

## Verification

At least one positive contract test and one hostile mutation or security-negative test must demonstrate the boundary. Deterministic replay must preserve the semantic result when all material inputs are unchanged.

## Related

- [[00_MOC]]
- [[ACL_05_IMMUTABLE_BATCH_AND_STORE]]
- [[IMMUTABLE_RESEARCH_BATCH]]
