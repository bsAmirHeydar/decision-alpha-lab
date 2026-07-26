---
id: SAED-C64CBD9059
title: "Dominance, Pruning, and Search-Space Control"
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
  - treatment
  - search-space
---

# Dominance, Pruning, and Search-Space Control

## Safe Pruning

A candidate may be pruned before training for semantic incompatibility, impossible geometry, unavailable features, broker infeasibility, exact duplication, cost infeasibility or deterministic dominance under identical outcomes.

## Unsafe Pruning

Do not prune because a protected validation period looked bad, because an analyst dislikes the candidate after observing outcomes, or because it increases the number of trials to be counted.

## Hierarchical Search

1. Compare entry mechanisms under controlled stop/exit.
2. Compare payoff profiles for shortlisted entries.
3. Compare exit/management variants.
4. Run bounded joint tournament on the final shortlist.

This reduces combinatorial explosion while preserving honest selection lineage.
