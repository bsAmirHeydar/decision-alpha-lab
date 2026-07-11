---
type: strategy-factory-document
status: canonical
title: "Setup Discovery and Rule Search"
tags:
  - strategy-factory
---

# Setup Discovery and Rule Search

The factory supports explicit setups and discovery, but keeps discovery from contaminating confirmation.

## Two lanes

The fixed-setup lane tests rules supplied by the architect exactly as written. The discovery lane searches bounded feature interactions or policy combinations. Discovery results become new hypotheses and must be frozen before a fresh confirmation period.

## Search methods

Start with base rates, one-feature buckets, monotonic threshold scans, and simple interactions. Then use regularized models or tree-based challengers. Search depth, trial count, and selection metric are declared before execution.

## Human review

The system may surface candidate conditions, but the architect decides whether they correspond to a coherent market mechanism or are likely artifacts. A discovered rule is not merged into the original canon; it becomes a separate version or overlay.

