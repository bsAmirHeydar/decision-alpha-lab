---
tags:
  - nds
  - f2
  - point2
  - execution-adapter
  - root-fix
status: canonical
---

# NDS F2 Canonical Point-2 Projection Root Fix

## Locked interpretation

```text
Phoenix F2 body:
Origin → Leg1 → Waist → Leg2

then Phoenix post-flag phase:
internal 1/2 or Waist-break branch

then Phoenix confirmation:
return through original Leg2 / flag end
```

The execution layer does not redefine any of these stages.

```text
projected branch Point 1 = existing F2 flag Waist
executable Point 2 = strict limit fill beyond that Waist
Stop = behind direct parent F1 Waist
RR/fixed target = original F2 flag end
```

## Root protections

- Entry offset is at least Phoenix boundary epsilon plus one trade tick.
- Every pending order is bound to the exact F2 body identity.
- Leg2 extension, F2 confirmation, invalidation, disappearance, or supersession cancels only that order.
- Dynamic exit orders with broker TP `0` still cancel before fill when the original F2 flag end is consumed.
- Pending source reconciliation runs once per closed entry-timeframe bar, never as a per-tick F detector.

## Core files untouched

The Flag Body, Internal Count, F1/F2/F3 lifecycle, and Sequence engines remain unchanged.

## Links

- [[NDS F2 Waist-Break Point2 Limit Setup]]
- [[../../nds_entry_architecture/f2_waist_break_point2_limit/18_canonical_point2_projection_root_fix|Detailed root-fix contract]]
- [[../../flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]]
