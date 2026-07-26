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

## Canonical Seed-Owned Sequence Rule — Current Authority

This section supersedes any earlier wording that implies unrestricted end-backward branch enumeration for the production Hook view.

Hook sequence counting starts from a raw same-side node list ordered from old to new. The raw list is scoped inside a Hook origin boundary context.

For a positive / low-side Hook:

```text
raw = valleys ordered old-to-new
first unused valley = node 1 of the next sequence
scan forward to the end of the raw list
each strictly lower valley becomes node 2, then node 3, then node 4, ...
```

For a negative / high-side Hook:

```text
raw = peaks ordered old-to-new
first unused peak = node 1 of the next sequence
scan forward to the end of the raw list
each strictly higher peak becomes node 2, then node 3, then node 4, ...
```

After a sequence is built, every node that participated in that sequence is marked as participated. A participated node may not become `node 1` of a later overlapping sequence. However, it may still appear as a continuation node (`2`, `3`, `4`, ...) in a later sequence if the forward strict-order scan naturally requires it.

This is a seed-ownership rule, not a full node-exclusion rule.

```text
participated node -> cannot restart as node 1
participated node -> may still be counted later as continuation evidence
```

The sequence must not stop at `2` if later valid continuation nodes exist. It must scan to the end of the scoped raw list and keep extending while the strict same-side rule continues to pass.

