# Concept Taxonomy

This file organizes the model into object layers.

## Layer 0: Raw Market Data

```text
Bar time
Bar high
Bar low
```

Only high and low are structurally consumed. Other bar fields may exist in platform data but are irrelevant to this model.

## Layer 1: Project Nodes

```text
Node
  side: HIGH | LOW
  time
  price
  L
  plateau metadata
  stable id
```

Nodes come from the existing project node module. The Flag Counting engine must reuse that logic instead of redefining it.

## Layer 2: Node Views

The system may build several node views by L.

```text
NodeView(L=2)
NodeView(L=3)
NodeView(L=5)
...
```

These views are not arbitrary smoothing. They are structural node sets under the project L rule.

## Layer 3: Flag Body Candidate

A body candidate is the first complete two-leg geometry.

```text
FlagBodyCandidate
  direction
  origin_node
  leg1_node
  waist_node
  leg2_node
  size
  L metadata
  owning phase context
```

A body candidate becomes meaningful only when Leg2 exists. Before Leg2, it is not a complete flag body.

## Layer 4: F-Level Object

The same body may serve as F1, F2, or F3 depending on sequence role.

```text
FObject
  level: F1 | F2 | F3
  body
  parent chain id
  status
  post-flag context
  confirmation/completion info
```

F-level is not a shape. It is a lifecycle role.

## Layer 5: Post-Flag Context

```text
PostFlagContext
  parent F object
  adverse nodes
  opposite nodes between adverse nodes
  hook branches
  deepest correction extreme
  50% cycle evaluation
  confirmation break candidate
```

This context must be stored because F2 and F3 origins are backfilled from it.

## Layer 6: Hook Branch

```text
HookBranch
  direction context
  adverse_side
  start_node
  extreme_node
  final_node
  numbered adverse nodes: 1..N
  N in {2,3,4} for readable view
  is_nd = N in {3,4} and 50% condition passes
```

A hook branch may share some nodes with another branch.

## Layer 7: Sequence Chain

```text
SequenceChain
  chain_id
  direction
  scale/context identity
  f1
  f2
  f3
  status
  phase boundary
  active child candidates
```

The chain owns the progression. It prevents arbitrary same-direction F1s from appearing in the middle of an active sequence.

## Layer 8: Audit Events

Every meaningful state transition should create an audit event.

Examples:

```text
NODE_EMITTED
F1_BODY_CANDIDATE_CREATED
F1_INTERNAL_12_FOUND
F1_CONFIRMED
F2_AUTHORIZED_BACKFILLED
F2_CANDIDATE_DIED_ORIGIN_PASSED
F2_REBUILT_FROM_PARENT_CONTEXT
F3_COMPLETED
F3_LOCKED_BY_OPPOSITE_F1
ND_HOOK_BRANCH_EMITTED
```

## Layer 9: Render Objects

Render objects are derived from emitted logical objects.

```text
RenderFlagBody
RenderFlagLabel
RenderInternalNumberLabel
RenderHookArc
RenderOriginMarker
```

Render objects must not alter logic.
