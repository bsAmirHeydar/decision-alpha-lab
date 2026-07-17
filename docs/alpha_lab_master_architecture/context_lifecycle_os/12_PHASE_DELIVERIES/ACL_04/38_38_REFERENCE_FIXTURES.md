---
title: ACL-04 — Reference Fixtures
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-04, phase-delivery]
---
# Reference Fixtures

## Decision

ACL-04 implements reference fixtures as part of the bounded Dual Setup Factory. The decision is accepted only at the `SETUP_DEFINITION_REFERENCE_ONLY` claim ceiling.

## Contract

The component is bound to the exact `ACL03_TO_ACL04` handoff, Context identity/version, ACL-00 permit, Search Authority and Treatment envelope. It may create Setup-definition evidence but may not modify ACL-03 IR, infer market truth, submit orders or activate capital.

## Inputs

- Content-addressed upstream artifacts and schema versions.
- Explicit owner and actor identity.
- Closed policy and security classification.
- Known-time-safe information or an explicit diagnostic-only classification.

## Processing and invariants

1. Resolve exact identities and verify SHA-256 bindings.
2. Reject unknown fields, atoms, actions, versions and paths.
3. Execute deterministic logic under declared budgets.
4. Preserve human and AI origin as provenance while using one Policy IR.
5. Emit stable reason codes and immutable evidence.
6. Prevent execution, network, secret and capital capabilities.

For this topic specifically, reference fixtures must remain reproducible, independently testable and reversible. No local success can broaden the phase authority ceiling.

## Failure semantics

Missing identity, stale handoff, invalid authority, incompatible schema, unregistered capability, future-derived non-diagnostic input, budget exhaustion, Treatment violation or output-integrity mismatch denies progression. ACL-04 does not repair failures with hidden defaults.

## Verification

The implementation is covered by schema checks, unit/contract tests, property or mutation tests where applicable, security-negative scanning, deterministic reference replay and delivery hash validation. Passing these checks proves mechanics only.

## Evidence and operations

Authoritative evidence is JSON under the generated ACL-04 output. Obsidian notes are projections. Corrections create a new version or superseding artifact; history is not overwritten.

## Residual boundary

External data quality, statistical edge, market-regime robustness, broker behavior, MQL5 runtime parity and production authorization remain unresolved by this note.

## Related

- [[ACL_04_PHASE_DELIVERY_MOC]]
- [[ACL_04_DUAL_SETUP_FACTORY]]
- [[DUAL_LANE_SETUP_FACTORY]]
