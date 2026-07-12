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
F2 confirmation node = F3 Leg1
after correction → TP at that node
retest → exit
```

## Critical distinction

The minimum-RR filter and RR-based Entry repricing always use the original F2 Leg2 known at setup creation. The dynamic F3 target does not exist at entry and may not be used for authorization.

## Runtime boundary

The fast tester does not build the full F3 pipeline. It uses the canonical identity equivalence `F3 Leg1 = F2 confirmation node`, then waits for adverse correction and the retest.

## Links

- [[NDS F2 Waist-Break Point2 Limit Setup]]
- [[NDS F2 RR Hedge and Parallel Contexts]]
- [[NDS F2 Overlap Wider and RR Repricing]]
- [Canonical dual-exit contract](../../nds_entry_architecture/f2_waist_break_point2_limit/12_dual_exit_fixed_f2_and_f3_flag_retest.md)
