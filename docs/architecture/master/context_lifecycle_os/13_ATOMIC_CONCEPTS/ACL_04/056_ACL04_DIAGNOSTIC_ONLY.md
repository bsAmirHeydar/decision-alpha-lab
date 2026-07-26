---
title: ACL-04 Diagnostic Only
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-04, atomic-concept]
---
# Diagnostic Only

## Definition

`ACL04_DIAGNOSTIC_ONLY` is the ACL-04 atomic concept for diagnostic only. It is intentionally narrow so schemas, code, policies, tests, reason codes and operator documentation use one meaning.

## Contract

- It is bound to an exact Context version and `ACL03_TO_ACL04` handoff when applicable.
- It is deterministic, attributable and replayable.
- Unknown, missing, stale or incompatible values fail closed.
- It cannot broaden Context semantics, known-time visibility, Treatment scope, runtime authority or capital authority.
- Material changes require semantic versioning, impact analysis and migration evidence.

## Invariants

The concept preserves the single-IR dual-lane design. Human and AI origin remains provenance; behavior identity is content-addressed. Machine artifacts remain authoritative and generated Obsidian notes remain projections.

## Failure behavior

A violation produces a stable ACL-04 reason code and denies candidate eligibility or phase progression. No permissive fallback, implicit coercion or silent repair is allowed.

## Verification

Coverage is provided by one or more closed-schema, unit, contract, property, mutation, security-negative, replay or delivery checks. Passing those checks establishes reference mechanics only.

## Claim boundary

This concept does not establish alpha, live parity, broker behavior, production readiness or capital authorization.

## Related

- [[ACL_04_ATOMIC_CONCEPTS_MOC]]
- [[ACL_04_DUAL_SETUP_FACTORY]]
- [[SETUP_POLICY_IR]]
