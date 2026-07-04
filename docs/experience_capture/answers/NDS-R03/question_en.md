# NDS-R03 — Node Identity, Node Cluster, and Node Replacement

## Question

Define node identity, node roles, node clustering, and node replacement in NDS.

## Why This Question Remains

Nodes can start CycleHooks, act as Extreme anchors, appear inside sequences, appear in different Hook/Rally contexts, and change practical validity depending on role. The system needs a stable node identity model.

## Answer Requirements

Please clarify:

- When does a node remain the same node?
- When does a node become consumed, invalidated, replaced, merged, or archived?
- If several nodes are near each other, are they separate nodes or a cluster?
- Does changing L create a new node identity or a different view of the same market area?
- How do node roles differ: origin, anchor, destination, internal, Extreme anchor, sequence node?
- If one node appears in multiple sequences, does it keep the same node ID?
- How should node identity behave across fractal scales?
- Which nodes must be drawn on chart?

## Expected Output

```text
node_identity_model_v1
node_role_taxonomy_v1
node_state_machine_v1
node_cluster_policy_v1
node_replacement_policy_v1
```
