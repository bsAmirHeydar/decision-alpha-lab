---
tags:
  - nds
  - f2
  - f3
  - exit
  - lineage
status: canonical
---

# NDS F2 Exact Per-Trade F3 Lineage Exit

## Core contract

```text
Position Ticket
→ its own Source F2
→ direct Child F3 of that Source F2
→ Child F3 Waist confirms correction
→ TP at that Child F3 Leg1
```

No position may use the latest same-direction F3 or the F3 belonging to another setup.

## Identity

Each context stores the exact F1/F2 event lineage, sequence, parent event, node IDs, times, setup hash, order ticket, position identifier, and position ticket.

## Fail-closed behavior

Ambiguous or missing lineage does not trigger a substitute exit. The position remains managed by its own stop until its own exact child F3 becomes available.

## RR boundary

The original F2 Leg2 remains the reference target for minimum RR and entry repricing. The future F3 target has no entry-authority role.

## Canonical document

- [Exact per-trade F3 lineage exit](../../nds_entry_architecture/f2_waist_break_point2_limit/14_exact_per_trade_f3_lineage_exit.md)
- [[NDS F2 Dual Exit - Fixed F2 or F3 Retest]]
