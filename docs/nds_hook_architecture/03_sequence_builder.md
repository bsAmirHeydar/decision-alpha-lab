# 03 — Sequence Builder

## Objective

Build Hook / CycleHook sequences from NDS nodes.

Every eligible node can start a CycleHook sequence, subject to the starter reuse rule.

## Starter Rule

A node can be the starter of a sequence once.

A node may appear in later positions of other sequences, but it should not repeatedly start new sequences after already serving as a starter.

## Positive Sequence Rule

Positive sequence:

```text
origin valley
then strictly lower valley nodes
```

Each new accepted X node must be lower than the previous accepted X node.

## Negative Sequence Rule

Negative sequence:

```text
origin peak
then strictly higher peak nodes
```

Each new accepted X node must be higher than the previous accepted X node.

## Multi-Sequence Rule

The system should allow multiple alive sequences at the same time.

Each sequence keeps its own identity.

Suggested object:

```text
CycleHookSequence
```

## Max Nodes Rule

If a sequence produces more than the allowed number of nodes, increase L until the maximum accepted node count is within the target range.

Existing captured principle:

```text
if max_nodes_per_sequence > 4:
    increase L until node_count <= 4
```

Default target:

```text
2 to 4 nodes
```

## Fixed-Origin vs Recalculated-Origin Views

The system should support two views:

### Fixed-Origin View

Used for:

```text
entry refinement
Extreme Near Death
local entry architecture
```

The origin remains fixed.

### Recalculated-Origin View

Used for:

```text
real structure
context
zone
fractal hierarchy
```

The origin can disappear or be replaced as structure is recalculated.

## Sequence Fields

Suggested fields:

```text
sequence_id
cyclehook_id
direction
origin_node_id
x_node_1_id
x_node_2_id
x_node_3_id
x_node_4_id
node_count
l_value
view_mode
is_alive
death_detected
closure_detected
created_at_bar
last_updated_bar
```

## Sequence Audit

Every accepted node should produce an audit row:

```text
sequence_id
candidate_node_id
accepted
rejected_reason
strict_rule_checked
previous_node_price
candidate_node_price
```
