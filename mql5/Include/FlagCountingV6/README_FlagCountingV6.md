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

## V6.1 repair notes

V6.1 fixes the first visual-audit issues:

- root F1 starts are gated by ND/Hook phase boundaries by default;
- F2 and F3 backfilled origins are bounded to the parent post-flag correction;
- F3 lock triggers must be future opposite confirmed F1s;
- raw seeds are hidden from the main chart by default;
- superseded lifecycle labels are hidden from the main chart by default;
- parent ids can be shown in labels to audit ownership;
- label stacking now uses a time/price cluster lane instead of `event_id % 8`.

## Semantic ownership repair defaults

The V6 default view is now stricter about sequence ownership:

- `InpRequireF1PhaseBoundary = true`
- `InpEnforceSingleChainPerDirectionScale = true`
- `InpMergeVisualDuplicateBodies = true`
- `InpDrawRawSeeds = false`
- `InpDrawLifecycleHistory = false`

This means a chart should show semantically owned structures rather than every
internal attempt.  Turn off the enforcement inputs only when auditing the raw
state machine.


## V6.2 semantic-origin repair

The default semantic view is now stricter about root F1 creation. A root F1 is not allowed to be created from arbitrary two-leg windows when no readable ND/Hook phase boundary is available. The old fail-open scan remains available through `InpAllowF1FailOpenWhenNoHook=true`, but it is intended for audit/debug only because it can create mid-move roots.

The sequence post-processor also has an optional global same-direction ownership gate (`InpEnforceSingleChainPerDirectionGlobal=true` by default). If a direction already has an active root chain, a later same-direction root is pruned unless an opposite F3 appears between the two roots. This implements the documented phase rule more strongly than the earlier per-scale-only pruning.
