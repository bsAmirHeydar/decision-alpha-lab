---
title: AI Setup Generation Policy
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-04, setup-factory]
---
# AI Setup Generation Policy

## Purpose

This contract governs deterministic AI candidate generation inside an explicit Search Authority. It is part of ACL-04 and therefore operates only after an exact `ACL03_TO_ACL04` handoff has been validated.

## Ownership and authority boundary

AI is a bounded proposal mechanism; it has no authority to redefine Context semantics, widen the Treatment envelope, self-promote a candidate, access execution, or learn online from production.

ACL-04 owns Setup definition mechanics. ACL-03 remains authoritative for Context semantics, occurrence identity, detector state transitions, feature ordering and known-time guards. ACL-05 owns immutable Batch freezing. No ACL-04 component may infer authority held by either adjacent phase.

## Required inputs

AI requests, registered generator manifests, finite parameter domains, budgets, seeds and content-addressed memory references. Every material input carries an exact identity, semantic version and SHA-256 digest. Missing or ambiguous identities are blockers, not warnings.

## Produced artifacts

candidate Policy IR documents and a complete search-exposure record. Structured JSON is authoritative. Obsidian notes are generated or reviewed projections and cannot mutate behavior.

## Deterministic processing contract

1. Validate closed schemas and reject unknown fields.
2. Verify the ACL-03 handoff digest and every bound upstream digest.
3. Verify the subject-bound ACL-00 permit and Search Authority.
4. Resolve only registered atoms, actions, generators and finite parameter domains.
5. Compile to `ACL04_SETUP_POLICY_IR` without dynamic evaluation.
6. Apply known-time, Treatment, risk, expiry, budget and conflict constraints.
7. Canonicalize behavior and compute content-addressed identity.
8. Preserve all source provenance and deduplicate equivalent behavior.
9. Record complete generation exposure and emit projections atomically.
10. Produce a bounded `ACL04_TO_ACL05` handoff.

## Non-negotiable invariants

- `live_order_submission_allowed=false` and `capital_activation_allowed=false` in every authority, receipt and handoff.
- Context semantics and ACL-03 IR are read-only.
- Human and AI lanes compile to the same IR and validation path.
- Unknown atoms, actions, fields, versions or digests fail closed.
- Future-derived predicates are forbidden except inside explicitly diagnostic baselines.
- Candidate eligibility means eligible for Batch definition only.
- Origin, author identity and provenance do not change behavior identity.
- Search exposure is recorded before downstream statistical interpretation.

## Failure semantics and reason codes

Failures are explicit and stable, including handoff mismatch, authority denial, unknown atom, arity mismatch, forbidden lane, parameter-domain violation, generation-budget exhaustion, Treatment-envelope violation, missing expiry, conflicting direction, unsafe path and output-integrity failure. A failed candidate remains evidence; it is not silently repaired into another behavior.

## Verification obligations

Unit tests cover compilation and constraints. Property tests cover canonical invariance and deterministic IDs. Mutation tests alter authority and digests to prove guards fail. Security-negative tests attempt dynamic evaluation and execution-capability leakage. Golden replay rebuilds the reference universe and compares candidate and handoff digests. Delivery validation checks every indexed file from a clean checkout.

## Evolution and migration

Additive optional fields require a compatible minor schema version. New required fields, atom semantics, canonicalization behavior or digest inputs require a major version, explicit migration, historical fixture replay, impact analysis and rollback. Existing evidence is always interpreted under its original contract version.

## Claim ceiling

`SETUP_DEFINITION_REFERENCE_ONLY`. Passing these mechanics does not establish alpha, data validity, broker parity, execution correctness, production security or capital authorization.

## Related

- [[ACL_04_DUAL_SETUP_FACTORY]]
- [[DUAL_LANE_SETUP_FACTORY]]
- [[ADR_006_DUAL_LANE_SETUP_SINGLE_IR]]
- [[ACL03_ACL04_HANDOFF]]
