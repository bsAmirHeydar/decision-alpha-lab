# 08 — Pending, Position, and Exit State Machine

## States

```text
DISABLED
→ NO_ELIGIBLE_SETUP
→ BLOCKED
→ PAPER_LIMIT
→ LIMIT_SENT
→ PENDING_HELD
→ POSITION_HELD_FIXED_R1
→ broker SL or TP terminal outcome
```

Shared recovery states include duplicate-pending reconciliation, pending cancellation after Hook death, foreign-position block, multiple-position invariant failure, and send failure.

## Pending state

A single managed pending order blocks all new Hook setups for the configured magic. Economic ownership is established by symbol and strategy Magic. After ownership is established, the broker comment is parsed only to recover the immutable lifecycle profile across restart or input changes. An unknown profile fails closed.

For a recovered `HOOK_864_CYCLE_R1` pending order, the core reads broker Entry, SL, and TP, verifies directional ordering and at-least-canonical 1R protection, and writes the actual broker geometry into the report. A managed fixed-R pending order with missing or invalid protection is cancelled as a risk-reduction action; if cancellation is not accepted, the lifecycle is blocked for operator reconciliation. The existing structural-death guard may also delete the order. The order is never repriced when X count or Terminal changes.

## Position state

For `HOOK_864_CYCLE_R1`, the core:

1. finds the managed position by symbol and magic;
2. reads broker open price, SL, and TP;
3. validates directional ordering;
4. calculates actual risk and reward distances;
5. requires actual reward to be at least configured one R;
6. reports `POSITION_HELD_BY_FIXED_R1_PROTECTION` when valid;
7. fails closed when protection is missing or invalid.

## Exit ownership

The broker-attached Stop and Target own the economic exit. Phase 55 does not send a market close on F123. The F event detector remains available for Phase 52 and is untouched.

## Restart behavior

On restart, the engine scans broker orders/positions before selecting a new Hook. Existing managed exposure wins over new setup creation. This preserves idempotency even when the in-memory report state is empty.
