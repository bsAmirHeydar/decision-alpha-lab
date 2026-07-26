---
title: ACL-07 — Binomial Evidence
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-07, validation]
---
# ACL-07 — Binomial Evidence

## Purpose

This note specifies binomial evidence for the accepted ACL-07 reference implementation. It is written as an operational Obsidian artifact rather than a superficial code summary.

## Contract

The artifact is identity-bound, schema-validated, digest-protected, deterministic and non-promotional. Missing or ambiguous evidence does not become a permissive default.

## Engineering requirements

- Preserve ACL-06 evidence byte-for-byte.
- Apply only registered gate semantics.
- Record explicit PASS, FAIL, UNKNOWN or NOT_APPLICABLE.
- Keep Diagnostic candidates non-selectable.
- Publish reason codes, lineage and residual risk.
- Deny order submission and capital activation.

## Verification

Unit, contract, negative, replay and delivery tests must exercise this concern. Passing reference tests proves mechanics only.

## Navigation

- [[00_MOC]]
- [[ACL07_UNIFIED_VALIDATION_RUNTIME]]
- [[ACL07_ACL08_HANDOFF]]
