---
title: ACL-00 Atomic Concept — Approval Replay Attack
status: accepted-reference-implementation
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, acl-00, atomic-concept]
---
# Approval Replay Attack

## Definition

Reuse of an approval against a changed digest, expired request or different transition.

## Invariant

This concept is versioned, attributable and evaluated fail-closed. It cannot independently grant capital authority or live-order permission.

## Implementation binding

The machine binding is provided by the ACL-00 schemas, policy catalogs and `src.engine.tooling.strategy_factory.acl_os.acl_00` package. Breaking semantic changes require a major contract version and migration evidence.

## Verification

Contract, mutation or security-negative tests exercise the relevant boundary. Passing local tests establishes reference mechanics only.

## Related

- [[00_EXECUTIVE_DELIVERY_INDEX]]
- [[ACL_00_CONSTITUTION_AND_AUTHORITY]]
