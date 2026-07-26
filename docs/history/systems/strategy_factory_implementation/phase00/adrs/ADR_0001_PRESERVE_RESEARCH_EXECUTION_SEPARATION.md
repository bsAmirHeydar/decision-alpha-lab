---
title: "ADR-0001 — Preserve Research/Execution Separation"
status: accepted
---

# ADR-0001 — Preserve Research/Execution Separation

## Context

The existing architecture states that Python owns research and MQL5 owns execution. The Strategy Factory will add shared decision, risk, paper, and broker-boundary modules, which could blur this separation if authority is not modeled explicitly.

## Decision

Preserve the separation as an authority hierarchy rather than a language slogan:

```text
Research and model artifacts: no capital authority
Decision runtime: recommendation/abstention authority
Risk engine: rejection/reduction authority
Execution adapter: request-construction authority
Broker boundary: order-send authority
```

Language choice does not grant authority. A Python broker adapter would still be execution code; an MQL5 feature calculator would still be research-derived logic.

## Consequences

- Every authority-bearing contract must be explicit.
- Order-send call sites are confined to a future approved boundary.
- Research artifacts cannot directly trigger broker calls.
- The Phase 00 authority scan becomes a recurring release control.
