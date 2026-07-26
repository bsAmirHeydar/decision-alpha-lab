---
title: ACL-14 Atomic Concept 001 — Acl13 Binding
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-14, atomic-concept]
---
# Acl13 Binding

## Definition

`ACL13_BINDING` is an atomic contract concept in ACL-14. It is represented explicitly in schemas, policies, reason codes, tests or immutable evidence artifacts.

## Invariant

The concept cannot silently grant pilot execution, prospective-evidence status, validation, runtime, live-order or capital authority.

## Failure semantics

Missing, ambiguous or incompatible material produces an explicit UNKNOWN, UNSATISFIED or fail-closed result rather than an optimistic default.

## Traceability

- [[ACL14_FIRST_REAL_CONTEXT_PILOT_RUNTIME]]
- [[ACL14_READINESS_GATE_REGISTRY]]
- [[ACL14_ACL15_HANDOFF]]
