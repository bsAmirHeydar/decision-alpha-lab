---
title: ACL-09 — Hostile Review
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-09, phase-delivery]
---
# ACL-09 — Hostile Review

## Decision

This artifact records the ACL-09 engineering decision for **Hostile Review**. The implementation preserves ACL-08 validation lineage, keeps UNKNOWN explicit, quarantines diagnostic evidence, aliases exact duplicates and emits only bounded non-executing planner proposals.

## Contract

Inputs are exact, versioned and digest-bound. Outputs are deterministic, append-only, closed-schema and atomically published. Missing or ambiguous evidence fails closed.

## Acceptance evidence

Acceptance requires unit, property-like replay, security-negative, prior-memory idempotency, duplicate-suppression, schema, delivery and direct ACL-08 regression tests.

## Authority boundary

Alpha inference, research execution, automatic scheduling, promotion, order submission, capital activation and doctrine amendment are prohibited.

## Related

- [[00_MOC]]
- [[ACL09_MEMORY_AND_ACTIVE_PLANNER_RUNTIME]]
