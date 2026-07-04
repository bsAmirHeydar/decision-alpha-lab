# DST-R03 — Normalized Interpretation

## Core Claim

Destination lifecycle must remain inside NDS.

The system should not introduce external target logic, generic technical targets, indicator targets, or non-NDS destination rules.

Destination repricing, completion, consumption, and weighting should be based on:

```text
the same NDS anatomy
the same NDS weights
the same NDS logic families
```

Recommended canonical rule:

```text
DestinationLifecycle = NDSAnatomy + NDSWeights + NDSLogic
```

There is no additional native destination ontology outside this.

## NDS-Only Destination Lifecycle

DST-R03 sets a boundary:

```text
No external destination model.
```

Destination candidates should be derived from and updated by the same internal system already defined in prior records:

```text
Hook
CycleHook
Node
Sequence
X/Y closure
F-counting
Rally
symmetry
ND / origin logic
parent-child fractal context
scenario constraints
zone logic
entry logic
optionality
convexity
```

If a destination cannot be expressed through this anatomy, it should not be treated as a native NDS destination.

## Same Weights and Same Logics

The user states that destination should use:

```text
same weights
same logics
```

This means destination scoring should not require a new unrelated scoring system.

It should reuse or derive from already established NDS weight concepts:

```text
constraint strength
scenario weight
zone weight
destination openness
context power
X/Y closure strength
multi-sequence closure strength
symmetry usefulness
parent context dominance
cost-to-potential quality
profit openness
```

Destination should be a downstream application of the same structural evidence, not a separate target-prediction engine.

## Destination Repricing

Repricing should occur when NDS anatomy changes.

Examples:

```text
new F-counting appears
new open one-two appears
higher Hook internal counting changes
destination weight changes
parent/child relationship changes
scenario weight changes
zone state changes
optionality opens or closes
profit path changes
```

Repricing should not happen because of arbitrary price levels outside NDS.

Suggested process:

```text
observe NDS structural update
recalculate destination candidate set
update weights
update destination openness
log repricing event
```

## Destination Completion and Consumption

Completion or consumption should be determined by NDS logic, not external target conventions.

Possible completion/consumption signals:

```text
the NDS reason for the destination is fulfilled
the relevant F-counting destination is reached or structurally consumed
the open one-two destination is resolved by later structure
the higher Hook internal count no longer points to the same destination
the destination no longer preserves profit openness
the destination becomes irrelevant due to updated scenario/zone context
```

The exact touch/pass-through mechanics remain trainable, but the logic source must remain NDS-only.

## Historical Preservation

If a destination candidate loses usefulness, it should not disappear from the audit history.

It should become historical.

Suggested states:

```text
DESTINATION_ACTIVE
DESTINATION_REPRICED
DESTINATION_CONSUMED
DESTINATION_COMPLETED
DESTINATION_INVALIDATED
DESTINATION_HISTORICAL
```

This supports training later.

## Opposite Destinations

Opposite-direction destinations should also be evaluated through the same NDS anatomy and weights.

No special external logic is needed.

They can affect:

```text
profit openness
risk of holding
partial exit logic
scenario relative weight
position management context
```

But they should be expressed as NDS destination candidates or opposite scenario destinations.

## Relationship to DST-R01 and DST-R02

DST-R01:

```text
destination is trainable and candidate-set based
```

DST-R02:

```text
exit policy should preserve profit openness and prefer partial close over default trailing
```

DST-R03:

```text
all destination lifecycle decisions must use the same NDS anatomy and weights
```

Together:

```text
DestinationCandidateSet
→ NDS-only weight updates
→ profit openness score
→ trained exit policy
```

## Machine-Readable Summary

```text
destination_lifecycle_source = NDS_ONLY

allowed sources:
    - NDS anatomy
    - NDS weights
    - NDS logic families

not allowed:
    - external target logic
    - non-NDS technical targets
    - indicator-based destinations
    - arbitrary profit targets as native logic

destination repricing = update by NDS structural changes
destination completion = fulfillment or consumption of NDS destination reason
```

## Short Formal Statement

Destination lifecycle in NDS must be built only from the existing NDS anatomy, weights, and logic families. There is no separate external destination logic. Repricing, completion, consumption, and invalidation of destinations should occur when the underlying NDS structures, weights, or scenario/zone conditions change. Destination candidates can be updated, weighted, consumed, completed, invalidated, or archived, but all of those transitions must be explained through NDS-native anatomy rather than external target rules.
