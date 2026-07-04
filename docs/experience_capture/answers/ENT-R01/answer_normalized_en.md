# ENT-R01 — Normalized Interpretation

## Core Claim

NDS must distinguish two different Extreme concepts:

```text
Hook Extreme
Entry-Level Extreme
```

They are not the same object.

The Hook Extreme is an internal structural extreme of a Hook/CycleHook.

The Entry-Level Extreme is an execution-refinement condition where the entry-scale CycleHook is extremely close to death, creating a small stop and a more convex trade.

Recommended canonical term:

```text
ExtremeNearDeathEntry
```

## Hook Extreme

A Hook Extreme is the opposite price extreme inside a Hook/CycleHook.

For a positive Hook that starts from a valley:

```text
Hook Extreme = highest price observed after the Hook origin valley and before the relevant touch/return
```

In more general terms:

```text
Hook Extreme = opposite extreme created by the CycleHook movement away from its origin
```

This belongs to the structure of the Hook/CycleHook itself.

It is not automatically an entry trigger.

## Entry-Level Extreme

An Entry-Level Extreme means:

```text
the entry-scale CycleHook has moved excessively close to its own death
```

This is the practical execution concept.

It is a near-death condition at the entry level.

Recommended object:

```text
ExtremeNearDeathEntry
```

Meaning:

```text
the lower-scale CycleHook is close enough to its death boundary that the stop can be placed very tightly
```

The purpose is not to identify the biggest opposite extreme of a Hook.

The purpose is to exploit a near-death structural condition with minimal risk.

## Difference Between Hook Extreme and Entry Extreme

### Hook Extreme

```text
structural opposite extreme inside Hook/CycleHook
belongs to Hook anatomy
describes how far the Hook moved away from origin
used for CycleHook structure, ND, closure, and zone logic
```

### Entry-Level Extreme

```text
execution-level near-death condition
belongs to entry refinement
describes how close the entry-scale CycleHook is to death
used for tight stop and convex payoff
```

Short distinction:

```text
Hook Extreme = opposite extreme of the Hook move
Entry Extreme = near-death entry anchor
```

## Extreme Near Death

The entry-level Extreme should be formalized as:

```text
Extreme Near Death
```

This means the entry candidate is useful because it is very close to invalidation/death.

That creates:

```text
small stop
clear invalidation
low cost
high convexity
```

This matches the broader NDS principle:

```text
potential over correctness
convexity before win rate
```

## Relationship to Zone

The Entry-Level Extreme should normally be searched for inside a higher-level Potential Zone.

Reason:

```text
Zone = where context becomes exploitable
Entry Extreme = precise low-cost anchor inside that exploitable area
```

Therefore:

```text
PotentialZone → lower timeframe refinement → ExtremeNearDeathEntry
```

An Entry-Level Extreme outside a valid zone should not automatically become tradable.

It may be logged, but trade permission should require a valid parent zone or parent scenario context.

## Entry Risk Geometry

The main purpose of Entry-Level Extreme is smaller risk.

Risk geometry:

```text
entry_price near death boundary
stop behind the relevant entry-scale death boundary
invalidation clearly defined
reward path comes from parent zone/scenario/destination
```

The stop should be as small as practical while respecting:

```text
entry-scale node/death boundary
spread
minimum broker stop distance
symbol tick size
execution safety buffer
```

Even though broker/execution details are not part of the ontology, they must be handled in the execution layer.

## Convex Exploitation

Entry-Level Extreme exists to improve convexity.

It improves convexity by:

```text
reducing stop distance
preserving reward potential from the parent zone
creating better cost-to-potential ratio
allowing repeated low-cost tests
```

The entry itself does not create the reward path.

The parent scenario, zone, destination, and optionality create the reward path.

The entry-level Extreme compresses the cost.

## Entry Authorization

Entry-Level Extreme should not authorize trade alone.

It should require:

```text
valid parent scenario
valid PotentialZone
entry-scale Extreme Near Death
clear invalidation boundary
acceptable stop distance
enough destination/optionality
```

Suggested states:

```text
ENTRY_EXTREME_CANDIDATE
ENTRY_EXTREME_INSIDE_ZONE
ENTRY_EXTREME_NEAR_DEATH_VALID
LIMIT_ENTRY_ALLOWED
ENTRY_EXTREME_VETOED
ENTRY_EXTREME_INVALIDATED
```

## Invalidation

An Entry-Level Extreme becomes invalid when the near-death structure dies or the parent opportunity is no longer valid.

Possible invalidation causes:

```text
entry-scale death boundary crossed
parent zone destroyed
parent scenario dead
entry cost no longer small
reward/optionality collapses
limit no longer relevant after price leaves the area
new lower-scale structure reprices the entry
```

The most important invalidation is:

```text
the entry-scale CycleHook crosses its death boundary
```

## Machine-Readable Summary

```text
HookExtreme:
  structural opposite extreme of Hook/CycleHook
  example positive Hook = highest price after origin valley before touch

EntryLevelExtreme:
  Extreme Near Death
  entry-scale CycleHook excessively close to death
  purpose = smaller stop and higher convexity

Entry permission:
  requires parent zone + near-death entry anchor + clear invalidation + acceptable cost/reward
```

## Short Formal Statement

An Entry-Level Extreme in NDS is not the same as a Hook Extreme. The Hook Extreme is the opposite extreme of a Hook/CycleHook movement, such as the highest price seen after a valley-origin Hook before the relevant touch. The Entry-Level Extreme is an execution-refinement concept: an Extreme Near Death, where the entry-scale CycleHook has become excessively close to its death boundary. This creates a much smaller stop and improves convexity. It should normally be used inside a valid Potential Zone, where the parent structure provides reward potential and the entry-level Extreme compresses the cost.
