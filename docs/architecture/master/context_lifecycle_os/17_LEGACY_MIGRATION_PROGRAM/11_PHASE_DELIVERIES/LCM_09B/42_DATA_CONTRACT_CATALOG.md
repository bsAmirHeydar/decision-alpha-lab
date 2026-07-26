---
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# Data Contract Catalog

## Canonical Setup package

Identity and lifecycle contract for one frozen Setup. Required blocks include immutable source binding, Context boundary, Treatment boundary, complete rule surface, blocker IDs, reason codes, authority envelope, and package digest. `REFERENCE_BLOCKED` is an accepted canonical accounting status, not an executable status.

## Context snapshot

Caller-supplied evidence consumed by the pure evaluator. It carries Context identity/version, occurrence identity, observed time, availability time, feature/state payload, known-time completeness, source digest, and snapshot digest. The evaluator owns no independent clock and rejects incomplete known-time evidence.

## Setup decision

Deterministic result with decision identity, sequence, state, reason codes, temporal evidence, prior decision digest, explicit `no_trade`, all-false authority fields, and decision digest. Event precedence is cancellation, expiry, invalidation, confirmation, trigger, eligibility, abstention, then blocked fallback.

## Adapter registration

Binds a Setup identity to its legacy source digest and declares input/output record contracts. `executes_legacy_source=false` is mandatory. A blocked adapter cannot normalize evidence. A future reference-ready adapter may normalize only evidence supplied by an external replay producer.

## Factory registration

Binds Setup identity, package path, package digest, visibility, blockers, and four false authority fields to `ACL04_LEGACY_REFERENCE_PORT_V1`. Registration makes an identity inspectable; it does not make it selectable, promotable, runnable, or tradable.

## Golden case and trace

Golden cases bind one snapshot to one expected decision. Golden traces bind ordered events and a digest-protected restart checkpoint. Because LCM-09A authorized no implementation, all emitted cases and traces are blocked evidence that proves fail-closed behavior rather than legacy parity.

## Parity record and registry

One record per Setup identity. A record is `PASS`, `FAIL`, `BLOCKED`, or `UNKNOWN`. Missing legacy evidence and unauthorized implementation produce `BLOCKED`. Aggregate success cannot override a hard mismatch or blocked mandatory dimension. Both JSONL detail and a digest-bound JSON registry are published.

## Variance decision

Owner-controlled, versioned adjudication surface for known differences. This delivery contains zero decisions and zero waived mismatches. The empty set is intentional: a blocker is not converted into an approved variance.

## Blocker record

Append-only identity-specific record with blocker code, source phase, severity, owner, resolution state, source evidence, and digest. Blockers survive package materialization, Factory visibility, acceptance reports, and handoff.

## Treatment dependency seed

One LCM-10A inventory seed per Setup identity. It lists required capabilities and explicitly forbidden Setup-core capabilities. It does not create a Treatment identity, order router, risk envelope, or execution object.

## Event ledger

Deterministic sequence of package-materialization events. Sequence numbers are contiguous and subject identities are unique. The ledger records what LCM-09B did; it does not replace source provenance.

## Provenance graph

Connects the accepted LCM-09A handoff, each frozen Setup identity, and each canonical package. Edge roles distinguish upstream authorization to attempt a bounded migration from package materialization. The graph does not assert behavioral equivalence.

## Artifact locator

`required_artifact_locator.json` provides exact stable paths and digests for every artifact name required by the phase specification. It prevents humans and tools from inferring locations from directory conventions.

## Output manifest and receipt

The manifest records every generated package file except itself and the receipt to avoid digest cycles. The receipt binds the upstream handoff, manifest, downstream handoff, counts, and all-false mutation/cutover declarations. Verification recomputes every listed byte digest.
