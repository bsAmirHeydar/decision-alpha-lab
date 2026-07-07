# Phase 38 — Immediate Valid Hook Doctrine

## Purpose

This document locks the production validity layer for Hook visualization and Hook-zone eligibility.

## Valid Hook Families

Only two Hook families are production-valid.

### 1. Immediate Hook After Opposing F3

A completed or locked F3 validates only the immediate next Hook on the same structural scale. The immediate Hook must be opposite to the F3 direction.

```text
completed/locked F3
→ immediate next Hook on same scale
→ Hook direction is opposite F3 direction
→ valid Hook
```

If the first Hook after F3 is not opposite, that F3 validates no Hook. Later Hooks are not rescued by the old F3.

### 2. Hook After Hook

Hook-2 is valid only when it starts exactly from the terminal node of Hook-1.

```text
Hook-1.resolve_node_id == Hook-2.origin_node_id
```

The previous Hook is displayed only as the required parent companion of a visible Hook-after-Hook child.

## Non-valid Hooks

All other Hook-like structures are debug structures, not production-valid Hooks.
