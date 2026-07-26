---
title: 04 Data Contract
status: accepted
version: 1.0.1
tags: [rthp, context, acl-02, english]
---

# 04 Data Contract

The default price basis is BID. Both symbols must use the same explicitly registered price basis for a relationship evaluation. Prices and reference levels are normalized to each symbol's registered tick size.

Stale or imputed observations are retained as evidence only. They cannot substitute for synchronized observations and cannot create a confirmed Context event.

## Machine-readable authority

`lab/11_strategy_factory/contexts/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1`
