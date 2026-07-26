---
tags:
  - nds
  - entry-execution
  - f2
  - f3
  - exit
status: canonical
---

# NDS F2 Dual Exit — Fixed F2 or F3 Retest

## Modes

### Fixed F2 end

```text
TP = original F2 Leg2
```

### F3 flag retest

```text
original F2 Leg2 = RR reference only
exact Source F2 → its direct Child F3
Child F3 Waist confirms the correction
TP = Leg1 of that same Child F3
retest → exit only for the bound position ticket
```

## Critical distinction

The minimum-RR filter and RR-based Entry repricing always use the original F2 Leg2 known at setup creation. The dynamic F3 target does not exist at entry and may not be used for authorization.

## Runtime boundary

Dynamic mode emits the direct child F3 lifecycle only. It binds that child through exact parent-event and sequence lineage, requires the Waist of that same child as the correction gate, and never shares one F3 across positions.

## Links

- [[NDS F2 Waist-Break Point2 Limit Setup]]
- [[NDS F2 RR Hedge and Parallel Contexts]]
- [[NDS F2 Overlap Wider and RR Repricing]]
- [Canonical dual-exit contract](../../nds_entry_architecture/f2_waist_break_point2_limit/12_dual_exit_fixed_f2_and_f3_flag_retest.md)
- [[NDS F2 Exact Per-Trade F3 Lineage Exit]]
