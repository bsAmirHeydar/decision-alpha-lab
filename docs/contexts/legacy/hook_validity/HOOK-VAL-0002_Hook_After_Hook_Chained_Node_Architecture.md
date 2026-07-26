---
type: architecture_note
id: HOOK-VAL-0002
title: Hook After Hook — Chained Node Architecture
domain: hook_validity
status: canonical_draft
related:
  - Valid Hook
  - Chained Hook
  - Hook Zone
  - Fractal Noise Control
---

# HOOK-VAL-0002 — Hook After Hook: Chained Node Architecture

## 1. Definition

A **Hook After Hook** is a valid second hook that begins exactly where the previous hook ends.

The key rule:

> The last node of Hook-1 must become the starting node of Hook-2.

This is not merely two hooks appearing close to one another. The two hooks must share a structural node. The terminal node of the first hook is recycled as the birth node of the second hook.

## 2. Why Shared-Node Chaining Matters

Without this rule, the system can count hooks in too many ways. Any internal swing may become a new hook candidate. The result is fractal over-counting.

The shared-node rule solves this problem by requiring lineage.

A valid chained hook must have:

- a previous valid hook,
- a terminal node from that hook,
- a new hook beginning from that exact terminal node,
- a continuous structural relationship between the two hooks,
- no arbitrary re-anchoring.

This creates a disciplined hook sequence.

## 3. What This Means Conceptually

The second hook inherits structural relevance from the previous hook. It is not an isolated shape. It is a continuation, transition, or reconfiguration of the prior hook's terminal condition.

The last node of the previous hook is important because it represents the point where the prior hook completed its structural statement. If the next hook begins there, the market is effectively building a new structure directly from the previous hook's endpoint.

That makes the second hook meaningful.

## 4. Validity Conditions

A Hook After Hook is valid only if all of the following are true:

1. Hook-1 is already valid.
2. Hook-2 begins from Hook-1's terminal node.
3. The terminal node of Hook-1 is not merely near the starting node of Hook-2; it is structurally the same node.
4. Hook-2 is not created by arbitrary fractal re-counting.
5. Hook-2 creates a zone with a possible entry boundary and an invalidation boundary.

## 5. Invalid Variants

The following are not valid Hook After Hook structures:

- Hook-2 starts near Hook-1's terminal node but not from it.
- Hook-2 is counted from an internal micro-swing unrelated to Hook-1.
- Hook-2 is forced by changing timeframe interpretation after the fact.
- Hook-2 is discovered only after a favorable move has already happened.
- Hook-1 itself was not valid.

## 6. Zone Implication

A valid Hook After Hook may generate a hook zone.

The zone is valid because the hook source is valid. The zone can be treated as a risk contract only if its boundaries are clear:

- the entry side is defined,
- the stop/expiration side is defined,
- the zone is not excessively wide,
- the context gives open reward potential.

If the second hook produces a broad or unstable zone, lower-timeframe refinement is required.

## 7. Risk Contract Interpretation

The Hook After Hook structure is especially useful because it can produce a chained risk logic.

Hook-1 creates a structural endpoint. Hook-2 begins at that endpoint and creates a new decision area. If the zone derived from Hook-2 is tight enough, it becomes a high-quality limit-entry candidate.

The trade thesis is not:

> There are two hooks, therefore we trade.

The thesis is:

> A valid chained hook has created a measurable zone where risk is bounded and reward can remain open.

## 8. Learning Implication

In the dataset, Hook After Hook should be labeled separately from generic hooks.

Suggested fields:

- `hook_validity_type = hook_after_hook`
- `previous_hook_id`
- `current_hook_id`
- `shared_node_id`
- `shared_node_time`
- `shared_node_price`
- `zone_id`
- `zone_width`
- `invalidation_price`
- `outcome_mfe`
- `outcome_mae`
- `mfe_mae_ratio`
- `time_to_expansion`

This allows the system to test whether chained hooks actually produce superior zones compared with rejected hook-like noise.

## 9. Final Rule

> A second hook is valid only when it is structurally born from the final node of the previous hook.

No shared terminal-start node means no valid Hook After Hook.
