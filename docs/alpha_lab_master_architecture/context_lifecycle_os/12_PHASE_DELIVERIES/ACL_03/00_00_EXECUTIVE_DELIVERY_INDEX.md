---
title: ACL-03 Executive Delivery Index
status: accepted-reference-implementation
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, acl-03, delivery-index]
---
# ACL-03 Executive Delivery Index

## Delivered capability

ACL-03 turns one exact, semantically approved ACL-02 Context package into a reproducible non-trading compilation bundle. The source is frozen and hashed; approval is bound to that digest; the compiler emits deterministic IR for Context detection, occurrence identity, causal time and feature order; least-privilege adapter contracts and closed schemas are emitted; positive, negative and ambiguous fixtures are replayed; a machine-readable onboarding matrix identifies every unimplemented dependency; and a bounded handoff allows ACL-04 to create Setup candidates without changing Context meaning.

## Hard authority boundary

ACL-03 does not train a model, test profitability, discover Treatment value, construct an immutable research Batch, compile runtime code, submit orders or activate capital. A successful compilation proves only deterministic reference mechanics and artifact integrity.

## Evidence inventory

| Evidence | Location | Purpose |
|---|---|---|
| Compiler kernel | `tools/strategy_factory/acl_os/acl_03/` | Deterministic orchestration and IR compilation |
| Policy-as-code | `registry/acl_os/acl_03/policies/v1/` | Fail-closed authority, security and evolution rules |
| Closed schemas | `registry/acl_os/acl_03/schemas/v1/` | Machine-enforced artifact contracts |
| Reference Context | `lab/11_strategy_factory/acl_os/fixtures/acl_03/valid_context/` | Approved deterministic source fixture |
| Golden compilation | `lab/11_strategy_factory/acl_os/fixtures/acl_03/reference_compilation/` | Reproducible expected output tree |
| Test suite | `lab/11_strategy_factory/acl_os/tests_acl_03/` | Unit, mutation, property, contract and security-negative checks |
| MQL5 mirror | `lab/11_strategy_factory/mql5/Include/AlphaLab/ACL_OS/ACL03/` | Static cross-language contract surface only |
| QA report | `ACL_OS_03_QA_REPORT.json` | Consolidated local evidence |
| Hash ledger | `ACL_OS_03_FILE_HASHES.sha256` | Delivery integrity |

## Main guarantees

1. Source mutation after approval invalidates compilation.
2. Output replacement is allowed only for a marked ACL-03 generated root.
3. No guard DSL is dynamically evaluated or converted into unrestricted code.
4. Occurrence identity and feature order are stable and version-bound.
5. Every adapter contract explicitly denies order submission and capital access.
6. Golden replay preserves event order, known-time monotonicity and deterministic transition choice.
7. Every generated artifact traces to source, plan, policy and compiler versions.
8. ACL-04 receives only bounded Setup-authoring scope.

## Navigation

- [[00_MOC]]
- [[ACL_03_CONTEXT_COMPILER_AND_ONBOARDING]]
- [[ACL_03_STATUS]]
- [[CONTEXT_COMPILER]]
- [[CONTEXT_ONBOARDING_FACTORY]]
