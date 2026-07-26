---
title: Phase 04 Closure and 86.4 First-Arrival Contract
status: canonical
version: 1.1.0
updated: 2026-07-16
---
# 18 — Phase04 Closure and First-Arrival Contract

## Ownership

Phase 55 does not own cycle discovery. The authoritative objects are:

| Semantic fact | Canonical owner |
|---|---|
| Hook identity and family | `FP_HookPhase02Sequence` |
| Origin, Crown and X count | `FP_HookPhase02Sequence` |
| Y intervals/opposite extremes | `FP_HookPhase03Record` |
| 50% X-closure lifecycle | `FP_HookPhase04Lifecycle` |
| Origin-return death | `FP_HookPhase04Lifecycle` |
| Closed-bar first arrival at 86.4 | `FP_NDSHook864CycleR1Evidence` |
| Tick/broker normalization and order lifecycle | existing NDS Hook trade adapter |

The evidence bridge is not a new engine. It receives existing Phase04 records plus the canonical closed-rate array and produces an immutable execution-evidence snapshot keyed by sequence identity.

## Intrinsic Phase02 gate

Before looking for runtime evidence, the adapter requires:

```text
valid == true
hook_failed == false
valid_hook_family == true
family allowed by existing HH/F3H policy
Phase02 terminal available
resolve_confirmed == true
cycle_crown_valid == true
x_count ∈ {3,4}
state ∈ {MATURE,CAPPED}
86.4 projection inside Origin–Crown
```

`retracement_ratio` remains available for audit, but it does not decide the post-closure first arrival.

## Canonical Phase04 gate

The exact matching Phase04 record must prove:

```text
record.valid == true
x_closure_candidate == true
x_closed == true
closure_retrace_ratio == 0.50 through locked config
origin_return_penetrated == false
x_count ∈ {3,4}
```

If the snapshot is absent, stale for another symbol/timeframe, or cannot be matched by sequence ID, origin node ID, origin time and direction, execution fails closed.

## First-arrival scan

Entry remains:

```text
Entry = Crown + 0.864 × (Origin − Crown)
```

For positive Hooks, the first arrival is the first closed bar at or after closure whose low is less than or equal to Entry. For negative Hooks, it is the first closed bar at or after closure whose high is greater than or equal to Entry.

```text
Positive: low <= Entry
Negative: high >= Entry
```

The scan includes the closure candle. This is a known-time rule, not a market prediction rule. When both conditions happen in the same candle, the system knows the close only after the candle is complete and therefore cannot claim an earlier pending order at 86.4.

## Evidence identity

`sequence_id` is retained for audit but is not cross-engine authority because it is an array-local index. A Phase04 record is matched to a Phase02 sequence using stable structural identity:

```text
scale_l
origin_node_id + origin_time + origin_price
direction
x_count and x1/x2/x3/x4 node IDs
cycle_crown_node_id + cycle_crown_time + cycle_crown_price
```

The evidence snapshot is also scoped to exact symbol and timeframe. A snapshot from another chart context cannot authorize a setup.

## Runtime outcomes

| Condition | Outcome |
|---|---|
| no evidence snapshot | blocked |
| Phase04 record missing | blocked |
| invalid Phase04 record | blocked |
| X not closed | blocked |
| origin return death | blocked |
| first 86.4 already touched | blocked |
| closed, alive, untouched, x3/x4 | eligible for existing execution gates |

Eligibility does not guarantee order submission. Existing one-exposure, one-attempt, price-side, stop/freeze, volume, margin, account, symbol, and send-authority gates still apply.

## Restart and determinism

The Phase04 evidence is reconstructed from canonical closed history. Existing pending/position ownership is recovered from Magic and the broker comment profile code before new-entry selection. A restart cannot change an already-owned position from fixed 1R to F123 exit or create a second x4 attempt after x3.

## Hostile tests

Required tests include:

- terminal ratio above 0.864 while Phase04 first arrival remains untouched;
- same-bar closure and 86.4 touch;
- later touch after closure;
- touch before closure only;
- no Phase04 record;
- invalid record;
- X not closed;
- origin-return death;
- x-count disagreement;
- symbol/timeframe mismatch;
- positive and negative symmetry.
