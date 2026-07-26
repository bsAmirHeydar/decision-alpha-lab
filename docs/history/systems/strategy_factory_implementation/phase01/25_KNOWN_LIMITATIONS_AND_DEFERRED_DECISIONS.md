# Known Limitations and Deferred Decisions

## FNV width

The stable ID is 64-bit and non-cryptographic. It is appropriate for idempotency at current scale but not an integrity signature. Cryptographic hashes remain separate lineage fields.

## Snapshot lookup

The MQL5 snapshot currently uses a dynamic array and linear lookup. A compiled fixed vector and indexed lookup belong to the feature-DAG and low-latency phases.

## Wire deserialization

Phase 01 provides deterministic emitters and Python serialization. A robust MQL5 JSON parser is intentionally not introduced into the live path. Later replay/import services may use CSV/JSONL readers outside the fast path.

## Decimal policy

Canonical JSON uses ten decimal places for foundation price output. Instrument tick normalization and exact decimal scaling belong to candidate/execution geometry phases.

## Clock conversion

This phase stores UTC and source lineage but does not calculate DST transitions. Phase 07 owns the market-clock implementation.

## Full contract family

Trade candidates, outcomes, models, action plans, execution intents, traces, telemetry, and promotion contracts are deferred to the phases that can define their invariants correctly.

## MetaEditor evidence

This Linux build environment cannot compile MQL5. Static compatibility passed, but local Windows compilation is a mandatory gate and is not represented as already completed.
