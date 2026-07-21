---
title: RTHP Source Freeze and Authority Binding
status: frozen
version: 1.0.2
---
# Source Freeze and Authority Binding

## Exact bindings

- Source snapshot digest: `sha256:418c9cbe3d35fab4483224ef3a086ffdc521a9a94d1d6daaeb261c3a3554ad18`
- Compiler version: `1.0.0`
- Context artifact: `CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1@1.0.2`
- ACL-03 permit action: `ACL03_COMPILE_CONTEXT`
- Semantic approval roles: `semantic_owner`, `independent_reviewer`

## Freeze semantics

The snapshot includes authored package files and excludes generated, report, intake, and cache directories according to the central ACL-03 source-freeze policy. A source mutation invalidates the snapshot-bound approval and requires a new approval and compilation receipt.

## Failure policy

Subject mismatch, action mismatch, source drift, open ACL-02 blockers, missing reviewer separation, or authority escalation fails closed. No permissive fallback exists.
