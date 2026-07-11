# Prohibition of broker order APIs

## Purpose

This document defines the Phase 17 contract for **prohibition of broker order apis** inside the MQL5-first Strategy Factory. Phase 17 is an execution-rehearsal layer: it consumes immutable Phase 16 execution intents and produces deterministic paper orders, fills, positions, transaction records, reconciliation evidence, and shadow comparisons. It has no broker-send authority.

## Canonical rule

Every decision is based only on information known at the processing timestamp. Input identity, runtime generation, policy hash, quote sequence, intent hash, and entity lineage remain attached to every derived artifact. A malformed, stale, conflicting, capacity-exceeding, or unauthorized input fails closed and is represented explicitly rather than being silently repaired.

## Runtime design

The MQL5 path uses typed structures, fixed-capacity arrays, direct method calls, and deterministic iteration. JSON parsing, filesystem access, dynamic loading, network calls, model training, and broker order functions are excluded from the quote-to-fill fast path. Python provides an offline conformance mirror, schema validation, golden replay, and reporting; it is not the live source of execution truth.

## State and audit implications

Order and position transitions are legal-state-machine transitions. Each accepted transition appends one transaction to a monotonic, hash-chained ledger. Repeated intents with identical identity and hash are idempotent. Repeated identity with a different hash is a hard conflict. Quote observations are deduplicated by sequence, scoped by symbol, and rejected when stale.

## Verification

Verification requires Python unit tests, schema parsing, golden fixture replay, a no-live-authority boundary scan, repository engineering-policy checks, and local MetaEditor compilation of the host, diagnostic, and self-test Expert Advisors. The local terminal compile result must be retained as evidence because this build environment cannot execute MetaEditor.

## Phase boundary

This topic does not authorize OrderCheck, OrderSend, asynchronous sends, broker position mutation, or live account risk. Those capabilities remain deferred to Phase 18 and must be introduced behind kill switches, circuit breakers, explicit mode authorization, retcode handling, reconciliation, and micro-live promotion gates.
