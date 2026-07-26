# 05 — Visualization and Diagnostics

## Objective

The user must be able to see the Hook architecture clearly on chart.

The first goal is not training.

The first goal is visual stabilization.

## Required Visual Layers

### CycleHook Origin

Draw origin node.

Label:

```text
HOOK O
```

### X Nodes

Draw accepted X nodes.

Labels:

```text
X1
X2
X3
X4
```

### Y Extremes

Draw opposite Extremes.

Labels:

```text
Y01
Y12
Y23
```

### ND

Draw ND area or ND marker.

Label:

```text
ND
```

### Death Boundary

Draw death boundary at origin penetration line.

Label:

```text
DEATH
```

### Closure

Draw closure marker when closure rule is satisfied.

Label:

```text
X CLOSED
XY CLOSED
```

### Hook Type

Draw type label:

```text
HOOK A
HOOK B
HOOK C
```

## Suggested Chart Objects

```text
trend lines between X nodes
trend lines between Y extremes
horizontal line for death boundary
text labels for sequence id
text labels for type and state
optional rectangle for ND zone
```

## Diagnostics Table / CSV

The expert should optionally export or print:

```text
cyclehook_id
sequence_id
direction
origin
x_nodes
y_extremes
node_count
l_value
x_closed
y_closed
xy_closed
hook_type
nd_active
death_detected
state
```

## Object Management

Objects must be namespaced and cleaned by display family.

Suggested prefixes:

```text
NDS_HOOK_
NDS_HOOK_POS_
NDS_HOOK_NEG_
NDS_HOOK_X_
NDS_HOOK_Y_
```

## Visual Priority

Avoid chart pollution.

Recommended toggles:

```text
show only latest N sequences
show only alive hooks
show historical hooks
show debug labels
show closure labels only
```

## Acceptance Criteria

The chart should make it possible to answer:

```text
Where did the Hook start?
Which nodes are counted?
Where are the opposite Extremes?
Is it alive or dead?
Has X closed?
Has XY closed?
Is it Type A, B, or C?
Where is ND?
Where is the death boundary?
```
