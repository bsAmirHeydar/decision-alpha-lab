---
title: ACL-03 — CLI and Operator Workflow
status: accepted-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, acl-03, context-compiler, onboarding]
---
# CLI and Operator Workflow

## Purpose

This note defines the enforceable ACL-03 treatment of **cli and operator workflow**. ACL-03 compiles an exact, semantically approved ACL-02 Context package into deterministic, closed-schema, non-trading intermediate representations and onboarding evidence. The compiler does not broaden Context doctrine, invent Treatment authority, train a model, establish statistical edge, generate unrestricted executable code, or authorize capital.

## Inputs

- Exact Context artifact identity and semantic version.
- Frozen source snapshot with SHA-256 inventory.
- ACL-02 readiness evidence with no open blockers.
- Subject-bound ACL-00 permit for `ACL03_COMPILE_CONTEXT`.
- Semantic owner and independent reviewer approval bound to the same source snapshot.
- Registered policy, schema and extension versions.

## Invariants

1. Any source mutation after approval invalidates compilation authority.
2. Unknown fields, unresolved identities, unsafe paths and unregistered extensions fail closed.
3. Detector behavior is represented as declarative IR; dynamic evaluation and direct code generation are forbidden.
4. Known-time guards are explicit, ordered and non-bypassable.
5. Generated artifacts are atomic, content-addressed, reproducible and never hand-edited.
6. Adapter contracts carry least privilege and explicitly deny order submission and capital access.
7. Golden replay proves deterministic mechanics only; it does not prove alpha or real-market validity.
8. ACL-04 receives a bounded handoff and cannot alter Context semantics.

## Failure semantics

The operation stops with stable reason codes for authority mismatch, semantic approval mismatch, source drift, IR ambiguity, duplicate transitions, incomplete occurrence identity, missing clock relations, unsafe feature views, replay failure, path escape, symlink use, unregistered adapter capabilities or output integrity failure. No permissive fallback is allowed.

## Evolution

Additive IR fields require a compatible schema minor version and conformance tests. Breaking semantic or ordering changes require a new Context version, new source snapshot, new approval, migration impact analysis, replay regeneration and rollback evidence. Extensions use public ports and capability manifests; they may not import private kernel modules or escalate authority.

## Evidence

Machine-readable artifacts remain authoritative. Obsidian notes are generated or reviewed projections. Every output traces to the exact source snapshot, compiler plan, policy versions and compilation receipt.

## Related

- [[ACL_OS_HOME]]
- [[ACL_03_CONTEXT_COMPILER_AND_ONBOARDING]]
- [[CONTEXT_COMPILER]]
- [[CONTEXT_ONBOARDING_FACTORY]]
