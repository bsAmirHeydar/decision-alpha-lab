# FlagCounting V6 MQL5 Module

This is a new, modular implementation aligned with the V5 engineering documentation pack.

## Compile target

`mql5/Experts/FlagCounting/FlagCountingV6Experiment.mq5`

## Modules

- `FC6_Types.mqh` — canonical types, statuses, node identity, event identity.
- `FC6_NodeEngine.mqh` — L-rule node extraction from candle highs/lows, equal plateau merge, alternating view.
- `FC6_HookEngine.mqh` — branch-based ND/Hook counting, backward branch construction, 3/4-node ND rule.
- `FC6_FlagEngine.mqh` — two-leg flag body builder and F1/F2/F3 post-flag rules.
- `FC6_SequenceEngine.mqh` — F1 -> F2 -> F3 chain construction, backfilled child origins, F3 lock pass.
- `FC6_Renderer.mqh` — diagnostic rendering only; never invents logic.
- `FC6_Audit.mqh` — summary and verbose event/hook logs.

## Important contract implementation notes

- Nodes are extracted using the project L-rule from candle high/low values.
- Equal highs/lows are merged into a plateau node.
- Open/close/body/candle color are not used in structural logic.
- Strict break is required. Equality is not a break.
- F1 appears after a complete two-leg body.
- F2/F3 may appear from probable seed/leg because they are sequence-continuation stages.
- F2 is authorized only after F1 confirmation but is backfilled from post-F1 correction.
- F3 is authorized only after F2 confirmation but is backfilled from post-F2 correction.
- F3 qualification uses OR condition:
  - `F3.leg1_L >= ceil(0.80 * F2.leg1_L)` OR
  - `F3.flag_size > 0.70 * F2.flag_size`.
- ND/Hook is branch-based and rendered as gray arcs.
- Renderer draws all lines thin by default and uses detailed labels for auditability.

## Caveat

This is a large first implementation pass of the full contract. It is intentionally modular so each rule can be audited and refined without patching unrelated renderer logic.
