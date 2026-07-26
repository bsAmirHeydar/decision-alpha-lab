---
title: Event Source Descriptor
status: implemented
version: 1.0.0
phase: V4-03
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production-context-plane
tags: [saed-v4, v4-03, continuous-time-event-model]
---
# Event Source Descriptor

## Institutional invariant

The event model is a derived context-plane service. It may read an exact-version Twin Manifest, register immutable event streams, append hash-bound events, build deterministic projections and produce replay evidence. It cannot mutate UCEE truth, mutate the Twin Manifest, select a Treatment, allocate risk, activate runtime, access a broker, use the network or place an order.

## Canonical design

```text
Exact Twin Manifest
+ exact-version stream manifests
+ append-only bitemporal event envelopes
→ deterministic event ordering
→ watermark and lateness control
→ append-only corrections
→ event-state projection
→ replay and integrity receipt
```

## Required controls

- Every event carries event time, known time, source sequence, payload hash and source hash.
- Known time cannot precede event time.
- Stream versions cannot be rebound to different semantic content.
- Batch ingestion is atomic and duplicate handling is idempotent.
- Out-of-order events are governed by explicit watermarks and late-event policy.
- Corrections append evidence; they never mutate historical bytes.
- Multi-symbol alignment never invents a value through implicit forward fill.
- Projection state is reconstructed from exact events and exact temporal boundaries.
- Static MQL5 validation is not MetaEditor compile evidence.

## Failure posture

Unknown contracts, sequence gaps, source mismatches, invalid hashes, forbidden authority, correction conflicts and replay mismatch fail closed. Late events are either flagged, quarantined or rejected according to an immutable stream policy.

## Verification

Verification includes golden, negative, mutation, future-suffix, async alignment, correction, watermark, replay, schema, authority and MQL5 static tests. Actual MetaEditor compilation and runtime parity remain external evidence.

## Phase-specific interpretation

This chapter defines **Event Source Descriptor** as a closed, versioned and reproducible part of SAED V4-03. Its outputs are evidence-bearing artifacts, not trading authority. Implementations must preserve exact identities, temporal boundaries, lineage and reviewability across restart, reordering and independent reproduction.
