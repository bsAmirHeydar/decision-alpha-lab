---
tags: [exp0019, faerie-protocol, fp-i09, ledger, arbitration]
status: normative
phase: FP-I09
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Identity Collision Fail-Closed

## Purpose

Same ID with different payload blocks initialization and acceptance.

## Normative rules

1. Confirmed signal evidence is immutable and never deleted by quota or WW policy.
2. Quota identity is context epoch + trading day + canonical pair + owning A/L/N session.
3. Primary winner ownership is minimum `first_hunt_m1_time`; all later fields are technical tie-breaks only.
4. Both symbols, every enabled relation, both directions, historical N offsets, and direct WW setups compete in one pair-session pool.
5. Reservation is distinct from permanent consumption. FP-I09 emits only `RESERVED`; `CONSUMED` and `RELEASED` are forbidden while `FP-DEC-012` is open.
6. Every state mutation is represented by an append-only event with sequence, payload hash, prior-event hash, and event hash.
7. Repeated identical input is idempotent. Same semantic ID with different payload is a blocking collision.
8. A valid checkpoint is only an optimization; the immutable event stream remains rebuild authority.

## Deterministic algorithm

```text
Ingest ConfirmedSignal and its FP-I08 DirectionGateDecision.
Validate semantic identity and deduplicate.
Create EligibilityEvidence without changing the source signal.
Map the signal to one PairSessionQuotaKey.
Register the contender and compute the canonical rank key.
Resolve all known contenders for that quota key.
Reserve the minimum rank as the semantic winner.
Retain every other signal with explicit WW/quota/block disposition.
Append events; never rewrite prior events.
Materialize indexes and snapshot from canonical records.
On restart, validate checkpoint; otherwise rebuild from events.
```

## Invariants and edge cases

- Same-M1 ties use confirmation close, relation order, direction, hunter symbol, then signal ID.
- A WW direct setup competes normally but its weekly gate function remains independent of trade reservation.
- A signal suppressed by WW does not enter quota ranking but remains ledgered.
- A signal suppressed by quota references the winning signal and reservation.
- A late-arriving earlier Hunt may supersede a provisional, non-live reservation by appending a new generation; no event is deleted.
- Session sealing converts the current canonical reservation to final semantic arbitration evidence.
- A corrupt or incompatible checkpoint is rejected; it is never partially trusted.

## Evidence and diagnostics

Every output exposes config hash, source signal ID/hash, gate decision ID/hash, quota key, rank, winner linkage, reservation generation/finality, event-chain head, reason codes, module versions, and the unresolved consumption policy.

## Runtime authority

`NONE`. This phase cannot draw chart objects, submit or modify orders, open positions, call brokers, access networks, or select a permanent quota consumption policy.

## Navigation

- [[00_FP_I09_DELIVERY_MOC|FP-I09 Delivery MOC]]
- [[../../phases/FP_I09_SIGNAL_LEDGER_DEDUPLICATION_PAIR_SESSION_ARBITRATION_CHECKPOINTS_AND_RESTART|FP-I09 Program Phase]]
- [[45_HANDOFF_TO_FP_I10|Handoff to FP-I10]]
