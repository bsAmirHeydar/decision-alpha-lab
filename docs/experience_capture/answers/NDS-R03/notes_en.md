# NDS-R03 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
node identity model
node role taxonomy
role-specific validity model
strict node rule
node cluster as derived object
L-view dependent node replacement
multi-sequence node membership model
fractal node relation model
```

## Core Hard Rules

```text
ALL_NODES_HAVE_IDENTITY
NODE_IDENTITY_IS_STABLE
NODE_ROLE_IS_CONTEXTUAL
NODE_VALIDITY_IS_ROLE_SPECIFIC
NO_LENIENCY_IN_NODE_RULES
NODE_OBJECT_IS_NOT_DELETED_BY_ROLE_INVALIDATION
NEARBY_NODES_DO_NOT_AUTOMATICALLY_MERGE
NODE_CLUSTER_IS_DERIVED_GROUPING
MULTI_SEQUENCE_MEMBERSHIP_DOES_NOT_CREATE_NEW_NODE_ID
```

## Proposed Objects

```text
Node
NodeRole
NodeValidityState
NodeCluster
NodeLViewPresence
NodeSequenceMembership
FractalNodeRelation
```

## Proposed Datasets

```text
node_identity_model_v1.csv
node_role_taxonomy_v1.csv
node_state_machine_v1.csv
node_cluster_policy_v1.csv
node_replacement_policy_v1.csv
node_l_view_presence_v1.csv
node_sequence_membership_v1.csv
fractal_node_relation_v1.csv
```

## Proposed Fields

### Node

```text
node_id
symbol
scale_id
timeframe
node_type
node_level
node_price
node_time
created_by_l
created_by_axis
raw_identity_state
```

### NodeRole

```text
node_role_id
node_id
role_type
role_context_id
cyclehook_id
scenario_id
zone_id
sequence_id
entry_family_id
validity_state
valid_from_time
valid_until_time
invalidation_reason
```

### NodeCluster

```text
node_cluster_id
symbol
scale_id
cluster_price_low
cluster_price_high
member_node_ids
cluster_purpose
cluster_context_id
cluster_validity_state
```

### NodeSequenceMembership

```text
node_id
sequence_id
sequence_node_number
sequence_role
is_sequence_starter
sequence_axis
```

### FractalNodeRelation

```text
relation_id
parent_node_id
child_node_id
relation_type
price_distance
scale_relation
alignment_score
```

## Proposed Labels

```text
NODE_IDENTITY_STABLE
NODE_ROLE_CONTEXTUAL
ROLE_ACTIVE
ROLE_VALID
ROLE_INVALIDATED
ROLE_CONSUMED
ROLE_SUPERSEDED
ROLE_HISTORICAL_ONLY

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

NODE_CLUSTER_DERIVED
NODE_PRESENT_IN_L_VIEW
NODE_ABSENT_IN_L_VIEW
NODE_REPLACED_IN_RECALCULATED_L_VIEW
```

## Proposed AI Modules

```text
Node Identity Builder
Node Role Assigner
Node Role Validity Tracker
Node Cluster Builder
Node L-View Presence Tracker
Node Replacement Mapper
Node Sequence Membership Mapper
Fractal Node Relation Builder
Node Audit Renderer
```

## Architecture Consequence

The system should not store node meaning directly inside the node object.

It should store:

```text
Node identity table
Node role table
Node validity table
Node sequence membership table
Node cluster table
Node scale relation table
```

This keeps the core object strict while allowing rich context-dependent meanings.

## Open Questions

1. What exact rule creates the initial node_id?
2. Should node_id include symbol, scale, time, price, and L?
3. Should node identity be based on exact price/time or detected pivot object?
4. If L changes and a node disappears, should it be marked absent in L-view or superseded?
5. What exact rule defines node cluster width?
6. Should clusters be based only on price distance, never time distance?
7. Should cluster width depend on spread, cycle size, or symmetry?
8. Should an invalidated origin node remain usable as a historical destination reference?
9. Can a node lose one role and gain another later?
10. Can a node be active in child scale and historical-only in parent scale?
11. Should sequence membership allow one node to appear in multiple sequences as a later member?
12. Should one node be allowed to be both destination and Extreme anchor in different scenarios?
13. How should chart rendering handle many historical nodes?
14. Should node role validity be deterministic only, or can AI rank role strength?
15. Should the first implementation build the node identity/role schema before any entry logic?

## Attachment Index

No images were provided for this answer.
