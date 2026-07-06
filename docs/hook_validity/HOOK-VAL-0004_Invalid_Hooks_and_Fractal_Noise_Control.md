---
type: policy_note
id: HOOK-VAL-0004
title: Invalid Hooks and Fractal Noise Control
domain: hook_validity
status: canonical_draft
related:
  - Fractal Noise
  - Invalid Hook
  - Pattern Worship
  - No Stop No Trade
---

# HOOK-VAL-0004 — Invalid Hooks and Fractal Noise Control

## 1. Problem Statement

Fractal markets create infinite structural interpretation. A hook may appear on one scale, disappear on another, or become part of a larger pattern when viewed differently.

If the system accepts every hook-like shape, it becomes structurally unstable.

The result:

- too many zones,
- contradictory signals,
- weak invalidation,
- overtrading,
- poor dataset quality,
- pattern worship,
- false confidence.

## 2. Invalid Hook Definition

An invalid hook is any hook-like formation that does not belong to one of the two valid hook families:

1. Hook After Hook with shared terminal-start node.
2. Hook After Opposing F3.

A hook-like structure that fails both tests is not valid as a primary hook source.

## 3. Invalid Does Not Mean Invisible

Invalid hooks may still be visible. They may still be useful as weak context or visual annotation. But they must not generate primary tradable hook zones.

They can be stored as:

- observation-only hooks,
- weak hooks,
- candidate hooks,
- research hooks,
- lower-priority context.

But they must not be treated as valid risk-contract sources.

## 4. Why This Is Necessary

The strategy is zone-centric and antifragile. It needs fewer, cleaner, more measurable opportunities. An invalid hook often creates a zone that looks tempting but lacks structural lineage.

Such zones are dangerous because they may have:

- arbitrary start boundaries,
- unstable stop boundaries,
- unclear context,
- poor reward asymmetry,
- low repeatability.

## 5. Pattern-Worship Ban

The system must not trade hooks because they look aesthetically correct.

The rule:

> Pattern appearance is not evidence. Structural validity is evidence.

A hook-like shape is not enough. It must pass the validity policy.

## 6. Consequences for Zone Generation

Invalid hooks cannot generate primary hook zones.

If a hook is invalid:

- no direct limit order may be planned from it,
- no hook-zone risk contract may be created from it,
- no primary zone score may be assigned from it,
- it may only enter the system as weak context or research metadata.

## 7. Fractal Noise Filter

The system should apply a strict hook validity gate before zone construction:

```text
Raw hook-like candidate
→ validity test
→ valid family?
    yes → zone candidate allowed
    no  → observation only
```

This protects the strategy from uncontrolled fractal expansion.

## 8. Learning Policy

Invalid hooks should still be logged, but separately.

Why?

Because the system should be able to test whether invalid hooks actually underperform valid hooks.

Suggested labels:

- `hook_validity = invalid`
- `invalid_reason = no_shared_node | no_opposing_f3 | ambiguous_anchor | hindsight_count | no_stable_zone`
- `zone_allowed = false`
- `observation_only = true`

This creates an empirical path to confirm or refine the validity filter without letting invalid hooks contaminate the primary trading logic.

## 9. Final Rule

> The system must prefer missing some hooks over trusting structurally unstable hooks.

In this architecture, fewer valid hooks are better than many ambiguous hooks.
