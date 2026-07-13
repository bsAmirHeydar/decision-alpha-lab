---
tags:
  - nds
  - architecture
  - f2
  - f3
  - hotfix
status: implemented
---

# NDS F2 Exact Per-Trade F3 Exit Hotfix

The dynamic exit is owned by the exact source lineage of each position:

```text
Position → Source F2 → Direct Child F3 → F3 Waist → F3 Leg1 TP
```

The implementation rejects generic latest-F3 and same-direction-F3 selection.

- [[../08_entry_execution/NDS F2 Exact Per-Trade F3 Lineage Exit]]
- [Engineering overlay](../../nds_hook_architecture/72_f2_exact_per_trade_f3_exit_hotfix.md)
