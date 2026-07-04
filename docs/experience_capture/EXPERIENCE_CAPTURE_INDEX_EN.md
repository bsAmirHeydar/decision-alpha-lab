# Experience Capture Index

## Captured Records

### NDS-R03 — Node Identity, Role, Cluster, and Replacement

Path:

```text
docs/experience_capture/answers/NDS-R03/
```

Summary:

Nodes are stable NDS objects. They exist as structural identities, and Hook/Rally/CycleHook definitions assign them different roles with different validity levels. There is no leniency in node rules: identity and validity must be strict. A node may become invalid in a specific role, but the node object remains in history. Nearby nodes should preserve separate identities and may be grouped only through derived clusters. Nodes appearing in multiple sequences keep one node ID with multiple sequence-role mappings.

Main derived architecture requirements:

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
