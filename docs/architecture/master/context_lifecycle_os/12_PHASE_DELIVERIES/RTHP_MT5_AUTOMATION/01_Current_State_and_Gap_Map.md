---
title: RTHP MT5 Automation — Current State and Gap Map
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, gap-map, current-state]
---

# Current State and Gap Map

## Existing assets that must be reused

The repository already contains:

1. Canonical RTHP Context package `CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1@1.0.2`.
2. ACL-03 compiled Context IR and onboarding evidence.
3. RTHP AI-input ContextPackage, feature descriptors, views, dependence clusters, task references, and label templates.
4. RTHP Train Activation that accepts local paired source artifacts and delegates fitting to existing trainer engines.
5. Immutable run evidence, hashing, verification, and no-trade boundaries.

## Actual missing capability

The missing capability is not a new AI engine. It is a context-owned, read-only source adapter and orchestrator that can:

- connect to an installed MetaTrader 5 terminal;
- resolve two selected broker symbols;
- retrieve closed M1 bars automatically;
- verify common historical coverage and quality;
- materialize canonical M1 source artifacts;
- hand those artifacts to the existing RTHP materialization and train-activation path;
- execute the existing validation, dataset, label, split, trainer, and evidence stages.

## Current contract mismatch

The existing RTHP Train Activation accepts paired local tick-like JSONL artifacts. The planned production acquisition path must not synthesize fictitious ticks from M1 OHLC. The context-owned activation layer must therefore gain a new source mode:

```text
PAIRED_M1_BAR_JSONL
```

or an equivalent immutable M1 bar artifact contract. This change remains inside the RTHP-owned activation package and does not alter shared engines.

## Gap closure statement

After this delivery is implemented, the operator should only choose:

- primary broker symbol;
- secondary broker symbol.

All remaining values should be resolved by versioned defaults, terminal metadata, source receipts, and existing research profiles unless a fail-closed ambiguity requires explicit operator input.
