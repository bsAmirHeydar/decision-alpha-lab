---
title: ACL-00 — Policy Bundle and Digest
status: accepted-reference-implementation
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, acl-00, governance, security]
---
# ACL-00 — Policy Bundle and Digest

## Purpose

Freezes policy-as-code documents into a canonical digest carried by every decision.

## Contract

The implementation is contract-first, versioned and closed by default. Unknown fields, unresolved identities, stale evidence, weak authentication, missing approvals, failed security controls, claim inflation and concurrency conflicts return a deterministic denial. No permissive fallback is available.

## Engineering rules

- Inputs are immutable references and timezone-aware records.
- Every decision carries the policy-bundle digest and stable reason codes.
- The requester, evidence producer, approver and security evaluator remain attributable.
- State mutation uses optimistic concurrency and occurs only after a complete ALLOW decision.
- An audit event is appended for both ALLOW and DENY outcomes.
- Capital activation and live-order submission remain false in this phase.

## Security posture

ACL-00 assumes every actor, plugin, artifact and request may be compromised. Authority is granted only by explicit capabilities; evidence cannot upgrade its own class; approvals bind the exact request digest; waivers cannot disable protected controls; and the audit chain detects modification or deletion. Production key custody is deliberately deferred to ACL-12 through a verifier port.

## Verification evidence

Unit, contract, mutation, security-negative, deterministic replay, CLI, MQL5 static and clean-delivery tests cover this topic. Passing these tests establishes reference control-plane behavior only; it does not establish statistical edge, runtime parity, broker behavior or production security.

## Extension boundary

Additive behavior enters through policy catalogs and schemas. Breaking semantics require a new major contract version, impact analysis, migration, compatibility period and rollback. Domain engines may request transitions but may not bypass this evaluator or write lifecycle state directly.

## Related

- [[ACL_00_CONSTITUTION_AND_AUTHORITY]]
- [[LIFECYCLE_CONSTITUTION]]
- [[AUTHORITY_AND_SEPARATION_OF_DUTIES]]
