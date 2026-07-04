# NDS-R02 — Normalized Interpretation

## Core Claim

In NDS, Hook and Cycle are technically the same algorithmic object.

They are two viewpoints or two names for the same structure.

The canonical object should be represented as:

```text
CycleHook
```

A CycleHook starts from a node, moves toward an opposite Extreme, and later returns toward the origin area into Near Death, or ND.

Any node can start its own CycleHook, including small nodes. The importance of that CycleHook depends on L, scale, sequence structure, symmetry, context, and zone relevance.

## Object Identity

Technical rule:

```text
Hook == Cycle
```

Recommended object name:

```text
CycleHook
```

Possible view labels:

```text
HOOK_VIEW
CYCLE_VIEW
```

The system may display both names, but the algorithmic object should be one.

## Positive and Negative CycleHooks

Positive CycleHook:

```text
origin = valley
counted nodes = valleys
node sequence direction = lower valleys
origin must not be crossed
```

Negative CycleHook:

```text
origin = peak
counted nodes = peaks
node sequence direction = higher peaks
origin must not be crossed
```

## CycleHook Lifecycle

Birth:

```text
Every valid node can be the origin of a CycleHook.
```

Alive:

```text
The CycleHook is alive while the origin node is not crossed and while the structure continues to produce valid Hook/Cycle behavior.
```

Opposite Extreme:

For a positive CycleHook:

```text
opposite_extreme = highest price observed between relevant valley nodes
```

For a negative CycleHook:

```text
opposite_extreme = lowest price observed between relevant peak nodes
```

Near Death / ND:

```text
ND = return toward the origin node without origin penetration
```

ND is not only a fixed distance rule. Its practical meaning depends on:

```text
sequence state
X/Y closure
L value
symmetry projection
context
zone
scale
```

Death:

```text
CYCLEHOOK_DEAD_BY_ORIGIN_PENETRATION
```

This connects to EXT-06:

```text
even one point beyond the origin node invalidates the CycleHook/Extreme anchor
```

New CycleHook:

```text
After death, a new CycleHook may form from a new valid node.
```

## Sequence Model

A CycleHook contains multiple sequences.

A sequence is a local node-counting chain inside the CycleHook.

Each sequence has its own numbering:

```text
sequence_node_number = 1, 2, 3, 4
```

Positive sequence construction:

```text
next valley must be lower than the previous accepted node in the same sequence
equal is not accepted
```

Negative sequence construction:

```text
next peak must be higher than the previous accepted node in the same sequence
equal is not accepted
```

Important clarification:

```text
A node can appear in multiple sequences as a later member.
A node cannot become a new sequence starter again if it has already served as a starter.
```

## L-Coefficient Policy

The L coefficient starts from 2.

Rule:

```text
L starts at 2.
If max_nodes_per_sequence > 4, increase L.
Continue increasing L until max_nodes_per_sequence <= 4.
```

The market structure does not change when L changes. L only changes which nodes are considered valid at that reading level.

## Two L Views

Fixed-Origin L View:

```text
origin remains fixed while L increases
```

Purpose:

```text
Extreme discovery
entry refinement
local execution precision
```

Recalculated-Origin L View:

```text
origin is recalculated after L changes
```

The previous origin may disappear if it is no longer a valid node at the higher L level.

Purpose:

```text
context reading
real structure
zone definition
cleaner higher-level interpretation
```

Both views should be preserved as separate views.

## Hook Closure

A CycleHook is considered closed when:

```text
a valid sequence reaches 3 or 4 nodes
and price retraces more than 50% of the distance between origin and opposite Extreme
```

Symmetry is not required for closure.

Symmetry is a projection/estimation feature, not a closure condition.

Closure states:

```text
HOOK_OPEN
HOOK_X_CLOSED
HOOK_Y_CLOSED
HOOK_XY_CLOSED
HOOK_STRONGLY_CLOSED
```

## X-Sequence and Y-Sequence

Every sequence has two possible readings:

```text
X-sequence
Y-sequence
```

X-sequence is built from the main counted nodes.

In a positive CycleHook:

```text
X = descending valley sequence
```

In a negative CycleHook:

```text
X = ascending peak sequence
```

X-sequences are not all equal. They exist on a spectrum.

Possible X quality factors:

```text
node count
price spacing
regularity
symmetry
cleanliness
closure depth
```

Y-sequence in positive CycleHook:

```text
The first Y value is the opposite Extreme between the CycleHook start and node 1 of that sequence.
Later Y values are the opposite Extremes between the sequence nodes.
```

For a positive Y-sequence, those opposite Extremes should step lower.

If any required Y step fails, the sequence is not a complete Y-sequence and remains X-like.

Y-sequence in negative CycleHook:

```text
Y is built from the opposite valleys between peak nodes.
For a negative Y-sequence, those opposite valleys should step higher.
```

If any required Y step fails, the sequence is not a complete Y-sequence and remains X-like.

## X/Y Closure Strength

If a sequence is closed from X only, the Hook has X-side closure.

If a sequence is closed from Y as well, the Hook has Y-side confirmation.

If both X and Y are closed, the reversal is stronger and should be labeled separately.

Important rule:

```text
the more X-like the structure, the stronger X closure is
the more Y-like the structure, the stronger Y closure is
X/Y closure should be scored, not only classified
```

## Symmetry

Symmetry is not a closure condition.

Symmetry is used to estimate possible reversal points, ND zones, zone boundaries, and Extreme entry accuracy.

The important symmetry dimension here is price distance, not time.

Symmetry can be measured through:

```text
price distance between nodes
price distance between legs
leg size symmetry in Y-sequence mode
confluence between projections from multiple sequences
```

## Adaptive Thresholds

The 50% Hook return and 90% Extreme/ND values are not hard constants.

They are baseline ideas that should become adaptive based on symmetry and structure.

Future model:

```text
hook_return_threshold = function(symmetry, sequence geometry, context)
nd_threshold = function(symmetry, sequence geometry, context)
extreme_width = function(symmetry, sequence geometry, spread, context)
```

The goal is to avoid missed trades from overly tight levels and too-early entries from overly loose levels.

## Hook Types A, B, C

Hook type is a broader structural view of the whole Hook, not the same thing as X/Y sequence closure.

For a positive Hook, define:

```text
O = Hook origin
N1 = node 1
N2 = node 2
N3 = node 3

E01 = highest price between O and N1
E12 = highest price between N1 and N2
E23 = highest price between N2 and N3
```

Type A:

```text
E12 > E01
and E23 > E12
```

Type A is strongest.

Type B:

```text
E12 > E01
```

Only the first condition is required.

Type C:

```text
neither Type A nor Type B structure is present
```

Type C is weakest.

For negative Hooks, the logic is inverted using the lowest opposite valleys between peak nodes.

## Four-Node Type Classification

Hook type is classically read as a three-node structure.

A four-node Hook can occur.

For four-node Hooks, type classification is not a strict mechanical sliding-window rule.

It is structure-based and approximate.

Classification priority:

```text
try Type A first
then Type B
then Type C
```

The classifier may ignore or down-weight one node to read the dominant overall three-node shape.

Human/contextual structural reading is the reference for the first version.

AI can later learn this classification through reviewed examples.

## Relationship Between Hook Type and X/Y Sequence

Hook type A/B/C and X/Y sequence closure are different layers.

Hook type A/B/C is a global structural classification.

X/Y sequence closure is an internal sequence-level closure model.

They should be stored separately:

```text
hook_type = A/B/C
x_sequence_strength = score/class
y_sequence_strength = score/class
xy_closure_state = class
```

## Short Formal Statement

Hook and Cycle are the same algorithmic object in NDS. A CycleHook starts from a valid node, moves toward an opposite Extreme, and later returns toward the origin into ND. Positive CycleHooks count descending valleys; negative CycleHooks count ascending peaks. Each CycleHook contains multiple sequences, each with local numbering and X/Y readings. L starts at 2 and increases until sequence node count is four or less, with separate fixed-origin and recalculated-origin views. Closure requires a sequence reaching three or four nodes plus more than 50% return toward the origin; symmetry is not required but helps project reversal zones and refine entries. Hook types A/B/C classify the broader structure, while X/Y closure scores internal sequence strength.
