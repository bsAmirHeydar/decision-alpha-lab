# NDS-R03 — Normalized Interpretation

## Core Claim

Nodes are stable NDS objects.

They do not lose their identity simply because their role changes.

A node exists as a node, and then receives different roles depending on its placement inside Hook, Rally, CycleHook, sequence, Extreme, destination, invalidation, context, and scale.

Therefore:

```text
node identity is stable
node role is contextual
node validity is role-dependent
```

## Node Identity Rule

Every detected NDS node should receive a stable identity.

The node itself should not be redefined as a different object merely because it appears in different structures.

A node can participate in multiple structures:

```text
CycleHook origin
sequence member
Extreme anchor
destination
internal node
parent/child context reference
```

The same node may hold several roles at the same time.

## Node Role Is Contextual

A node's meaning comes from where it sits inside Hook and Rally definitions.

The same node can have different significance depending on:

```text
whether it is part of X-axis Hook/node-counting
whether it participates in Y-axis Rally/F-counting
whether it is a CycleHook origin
whether it is an Extreme anchor
whether it is part of a sequence
whether it belongs to parent, current, or child scale
whether it sits inside a valid zone
```

This means the node table should separate identity from role.

Suggested separation:

```text
Node = stable structural point
NodeRole = contextual role assignment
NodeValidity = validity state for that role
```

## No Leniency / No Approximate Identity

The user explicitly states that there is no tolerance or leniency.

This should be interpreted as:

```text
node identity and validity rules must be strict
```

If a rule says a node is crossed, invalidated, or not valid in a role, the system should not soften the rule by saying it is almost valid.

This connects to EXT-06:

```text
one point beyond the cycle-origin node invalidates that origin role
```

However, that does not necessarily mean the raw node object disappears from history. It means that specific role or CycleHook validity is dead.

## Identity vs Validity

Important distinction:

```text
node identity remains in the database
role validity can change
```

For example, if a node is the origin of a CycleHook and price crosses it, then:

```text
node_id remains
origin_role_validity = invalidated
cyclehook_state = dead
```

But the historical node still exists for audit.

## Node Role Taxonomy

A single node may be assigned one or more roles.

Proposed roles:

```text
ORIGIN_NODE
CYCLEHOOK_ORIGIN_NODE
ANCHOR_NODE
EXTREME_ANCHOR_NODE
SEQUENCE_NODE
DESTINATION_NODE
INTERNAL_NODE
DEATH_BOUNDARY_NODE
PARENT_CONTEXT_NODE
CHILD_REFINEMENT_NODE
ZONE_BOUNDARY_NODE
```

Each role must have its own validity state.

## Role-Specific Validity

A node's raw existence does not imply that every role remains valid.

Example:

```text
raw node exists = true
origin role alive = false
Extreme anchor valid = false
destination role may still be historically relevant
```

Therefore, the system needs role-specific state.

Suggested validity states:

```text
ROLE_ACTIVE
ROLE_VALID
ROLE_INVALIDATED
ROLE_CONSUMED
ROLE_SUPERSEDED
ROLE_HISTORICAL_ONLY
```

## Node Consumption

The user did not introduce a soft consumption rule.

Given prior answers, the strongest confirmed invalidation rule is penetration.

Therefore, for now:

```text
touch alone should not automatically destroy raw node identity
penetration can invalidate a role when the role uses that node as a death boundary
```

Consumption should be treated as a separate role-state, not deletion.

## Node Replacement

If L changes and the node no longer appears in a higher-L view, the original node should not be erased.

Instead, the system should record:

```text
node exists in lower-L view
node absent from higher-L view
higher-L replacement candidate exists
```

This matches NDS-R02:

```text
fixed-origin L view preserves origin for entry/extreme
recalculated-origin L view may cause previous origin to disappear for context/zone
```

So replacement is view-dependent.

## Node Cluster

The user did not define node merging as a native rule.

Given EXT-07, nearby nodes can each be separate opportunities.

Therefore, the safest rule is:

```text
nearby nodes keep separate node identities
clusters may be created as derived grouping objects
clusters do not erase node IDs
```

A cluster should be a higher-level grouping, not a replacement for node identity.

Suggested object:

```text
NodeCluster
```

Purpose:

```text
group nearby nodes for region, confluence, anchor opportunity set, or zone logic
```

But individual nodes must remain auditable.

## Node in Multiple Sequences

A node may appear in more than one sequence as part of different local sequence readings.

The node should keep the same `node_id`.

Sequence membership should be stored separately:

```text
node_id
sequence_id
sequence_role
sequence_node_number
```

This avoids duplicating the node object.

## Node Across Scales

If a lower-timeframe node and a higher-timeframe node appear near the same price region, they should not automatically be the same node.

They are separate node identities because they belong to different scale IDs.

However, they may be linked through a relation:

```text
fractal_node_relation
parent_child_node_alignment
same_region_node_cluster
```

So:

```text
same price area across scales = relation or cluster
not identical node_id
```

## Chart Audit

Since nodes are core NDS objects, the system should be able to draw all nodes when needed.

But for practical chart audit, active views should prioritize:

```text
CycleHook origin nodes
Extreme anchor nodes
sequence nodes
destination nodes
death boundary nodes
zone boundary nodes
parent-context nodes
```

Historical/inactive nodes can be hidden by default but must remain available for audit.

## Machine-Readable Summary

```text
Node = stable identity object
NodeRole = contextual assignment
NodeValidity = role-specific state
NodeCluster = derived grouping, not identity replacement
LView = determines which nodes are visible/valid in that view
Scale = separates node identity across timeframes
```

## Short Formal Statement

Nodes are stable NDS objects. They exist as structural identities, and Hook/Rally/CycleHook definitions assign them different roles with different validity levels. There is no leniency in node rules: identity and validity must be strict. A node may become invalid in a specific role, but the node object remains in history. Nearby nodes should preserve separate identities and may be grouped only through derived clusters. Nodes appearing in multiple sequences keep one node ID with multiple sequence-role mappings.
