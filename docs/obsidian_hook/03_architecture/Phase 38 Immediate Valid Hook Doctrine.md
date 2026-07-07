# Phase 38 Immediate Valid Hook Doctrine

## Rule A — Immediate F3 Hook

```text
F3 completed/locked
first Hook after F3 on the same scale
Hook.direction == -F3.direction
```

## Rule B — Hook After Hook

```text
previous.resolve_node_id == current.origin_node_id
```

No other Hook family is production-valid.
