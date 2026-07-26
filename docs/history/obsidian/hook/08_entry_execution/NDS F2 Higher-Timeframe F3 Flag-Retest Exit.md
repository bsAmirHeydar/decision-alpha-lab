---
title: NDS F2 Higher-Timeframe F3 Flag-Retest Exit
status: implemented
version: 1.0.0
updated: 2026-07-12
---
# NDS F2 Higher-Timeframe F3 Flag-Retest Exit

## Contract

```text
Lower-TF F2 Point-2 position
→ wait for first same-direction canonical HTF F3 after entry
→ lock its exact Leg1
→ wait for the Waist of that same F3
→ arm TP at the exact Leg1 endpoint
→ close only the bound position ticket on retest
```

Default exit timeframe:

```text
PERIOD_H1
```

## Inputs

```text
InpF2BTExitMode = FP_NDS_F2_EXIT_HIGHER_TIMEFRAME_F3_FLAG_RETEST
InpF2BTF3ExitHigherTimeframe = PERIOD_H1
```

## RR boundary

The HTF F3 target is not known at entry. Minimum RR and entry repricing remain anchored to the original lower-timeframe F2 Leg2 endpoint.

## Per-trade identity

Each position stores its own HTF F3 sequence, scale, Leg1 node, Waist node, dynamic target, and TP state. Shared mutable exit state is forbidden.

## Authority

- [[../../nds_entry_architecture/f2_waist_break_point2_limit/15_higher_timeframe_f3_flag_retest_exit|Detailed engineering contract]]
- [[NDS F2 Exact Per-Trade F3 Lineage Exit]]
- [[NDS F2 Higher-Timeframe F-Phase Filter]]
