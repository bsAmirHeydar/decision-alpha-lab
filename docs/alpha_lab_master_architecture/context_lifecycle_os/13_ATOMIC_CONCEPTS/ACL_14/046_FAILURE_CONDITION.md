---
title: ACL-14 Atomic Concept 046 — Failure Condition
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-14, atomic-concept]
---
# Failure Condition

## Definition

`FAILURE_CONDITION` is an atomic contract concept in ACL-14. It is represented explicitly in schemas, policies, reason codes, tests or immutable evidence artifacts.

## Invariant

The concept cannot silently grant pilot execution, prospective-evidence status, validation, runtime, live-order or capital authority.

## Failure semantics

Missing, ambiguous or incompatible material produces an explicit UNKNOWN, UNSATISFIED or fail-closed result rather than an optimistic default.

## Traceability

- [[ACL14_FIRST_REAL_CONTEXT_PILOT_RUNTIME]]
- [[ACL14_READINESS_GATE_REGISTRY]]
- [[ACL14_ACL15_HANDOFF]]
