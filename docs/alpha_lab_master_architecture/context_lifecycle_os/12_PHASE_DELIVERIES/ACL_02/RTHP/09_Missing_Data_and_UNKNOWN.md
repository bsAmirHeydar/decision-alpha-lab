---
title: 09 Missing Data and UNKNOWN
status: accepted
version: 1.0.1
tags: [rthp, context, acl-02, english]
---

# 09 Missing Data and UNKNOWN

When one symbol lacks a valid observation at the synchronized M15 cut, the last available observation may be retained with `STALE_OR_IMPUTED`, but the relationship remains `UNCONFIRMED` and `confirmed_context_event=false`.

The evaluator must re-run when synchronized real data arrives. UNKNOWN, partial history, stale data, and invalid configuration remain explicit; none may be coerced to a negative result or default success.

## Machine-readable authority

`lab/11_strategy_factory/contexts/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1`
