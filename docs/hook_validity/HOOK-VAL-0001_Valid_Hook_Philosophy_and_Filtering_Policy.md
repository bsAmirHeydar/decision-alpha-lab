---
type: architecture_note
id: HOOK-VAL-0001
title: Valid Hook Philosophy and Filtering Policy
domain: hook_validity
status: canonical_draft
related:
  - Hook After Hook
  - Hook After Opposing F3
  - Fractal Noise
  - Zone as Risk Contract
  - Antifragile Limit Entry
---

# HOOK-VAL-0001 — Valid Hook Philosophy and Filtering Policy

## 1. Core Problem

The hook concept is powerful, but it is also dangerous if left unconstrained.

Because market structure is fractal, a trader or algorithm can count hooks almost anywhere. On one scale a movement can appear as a hook, while on another scale the same movement can appear as a minor pause, a weak pullback, a continuation fragment, or a meaningless internal fluctuation. This creates an immediate architectural problem:

> If every hook-like structure is accepted, the system becomes noisy, over-fractal, unstable, and internally contradictory.

The purpose of the Hook Validity Layer is to separate **structurally meaningful hooks** from **fractal hook noise**.

## 2. The Strategic Reason for Restriction

Alpha Lab is not designed to worship patterns. It is designed to convert market structure into bounded-risk, open-reward opportunities. A hook is not valuable merely because it looks like a hook. A hook is valuable only if it creates a reliable zone source with a defensible entry boundary and a meaningful invalidation boundary.

Therefore, a hook must pass a structural validity filter before its zone can be trusted.

## 3. The Two Valid Hook Families

Only two hook families are considered valid by default:

### 3.1 Hook After Hook

A second hook becomes valid when it is chained directly to the previous hook.

The defining condition:

> The terminal node of the previous hook must be the starting node of the next hook.

This creates a structural chain rather than an arbitrary independent count. The new hook is not simply another hook-like shape. It is a continuation of a prior hook sequence through a shared node.

### 3.2 Hook After Opposing F3

A hook becomes valid when it appears after an opposing F3.

Example:

- A bearish F3 prints or becomes structurally established.
- After that bearish F3, a bullish hook appears.
- That bullish hook is valid because it emerges from the broad reversal field or exhaustion environment created by the opposing F3.

The opposing F3 gives the hook a meaningful structural background. The hook is not floating in isolation; it appears after an extended or unstable phase where reversal potential is already conceptually open.

## 4. What Becomes Invalid

All other hook-like formations are invalid by default as primary zone sources.

This does not mean they do not exist. It means the system must not rely on them for direct limit-entry zones.

Invalid hooks may still be used as:

- visual context,
- weak observations,
- secondary annotations,
- lower-priority data points,
- manual review candidates,
- future research candidates.

But they must not be treated as strong tradable hook zones.

## 5. Why This Matters for Zones

A zone derived from an invalid hook is also invalid as a primary hook zone.

The rule is strict:

> Hook validity comes before hook-zone validity.

The system must not ask whether the zone looks attractive before it confirms whether the hook source is structurally valid. If the hook source is invalid, the zone cannot be trusted as a primary risk contract.

## 6. Antifragile Interpretation

This restriction is not a reduction of opportunity. It is a reduction of false opportunity.

A system that accepts too many hooks appears active, but its activity is fragile. It creates too many entries, too many ambiguous zones, too much contradictory context, and too much exposure to patterns that have no stable structural contract.

An antifragile system prefers fewer but cleaner candidates:

- fewer hook zones,
- better structural lineage,
- clearer invalidation,
- less fractal confusion,
- better learning samples,
- cleaner failure analysis.

## 7. Final Principle

The hook is not the edge by itself.

The edge comes from a valid hook that creates a bounded-risk zone inside a context where the reward can remain open.

Therefore:

> Valid hook first. Tradable zone second. Limit entry third. Open profit management fourth.
