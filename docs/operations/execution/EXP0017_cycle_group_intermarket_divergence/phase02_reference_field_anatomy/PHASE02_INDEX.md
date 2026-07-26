# EXP0017 Phase 02 — Reference Field Anatomy

Phase 02 adds the first price-structure layer on top of Phase 01 Time Anatomy.

The robot still does **not** trade, does **not** detect hunts, and does **not** build divergences. Its only task is to build a clean same-day reference field for every enabled Cycle Group (CG) and for both configured symbols.

## Main outputs

- a standalone MQL5 expert: `EXP0017_CG_Reference_Anatomy.mq5`
- a reference-field module under `mql5/Include/IntermarketDivergenceExecution/CG/`
- same-day previous-cycle high/low extraction for both symbols
- M1-based aggregation so non-standard CGs such as `cg_3m`, `cg_9m`, `cg_18m`, `cg_72m`, and `cg_150m` are supported
- chart-panel visibility for current-cycle state and recent previous-cycle references
- extensive documentation and Obsidian knowledge-base material

## Phase boundary

This phase produces **reference candidates only**.

It must not answer:

- whether a reference has been hunted
- whether a divergence exists
- whether the signal is buy or sell
- whether a trade is allowed
- whether any CG is better than another
- whether any reference is higher quality than another

Those responsibilities are reserved for later phases.
