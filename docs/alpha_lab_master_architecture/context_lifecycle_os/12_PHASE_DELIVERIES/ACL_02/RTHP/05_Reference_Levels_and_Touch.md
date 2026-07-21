---
title: 05 Reference Levels and Touch
status: accepted
version: 1.0.1
tags: [rthp, context, acl-02, english]
---

# 05 Reference Levels and Touch

Each symbol owns its own High and Low for a given reference cycle. Correspondence is semantic, not numeric: the prices may differ.

A High touch occurs when the normalized observed price is greater than or equal to the symbol-local High. A Low touch occurs when it is less than or equal to the symbol-local Low. No close beyond the level is required, and no additional tolerance is added after tick-size normalization.

## Machine-readable authority

`lab/11_strategy_factory/contexts/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1`
