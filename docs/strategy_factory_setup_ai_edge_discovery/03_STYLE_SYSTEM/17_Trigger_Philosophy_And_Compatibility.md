---
id: SAED-3321F95C5E
title: "Trigger Philosophy and Compatibility Graph"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - trigger
  - compatibility
---

# Trigger Philosophy and Compatibility Graph

## Trigger Philosophies

- **Anticipatory:** enter at a declared level before full confirmation.
- **Context-Immediate:** Context completion itself authorizes activation.
- **Confirmatory:** wait for reclaim, close, breakout, retest or microstructure evidence.

## Compatibility Graph

Each Setup archetype publishes allowed combinations. The graph can include hard incompatibility, conditional compatibility and required capabilities.

Example:

| Payoff | Breakout | Market | Limit |
|---|---:|---:|---:|
| P1 Wide High-Hit | conditional | strong | strong |
| P2 Tight Convex Fixed | strong | conditional | strong |
| P3 Tight Convex Trail | strong | conditional | conditional |
| P4 Wide Open Trail | strong | strong | conditional |
| P5 Tight High-Hit | conditional | confirmation-only | strong |

This table is a prior, not evidence. The Experiment system may reject or refine compatibility only through versioned research.
