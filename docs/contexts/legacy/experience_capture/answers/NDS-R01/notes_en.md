# NDS-R01 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
canonical object model definition
axis model definition
fractal scale rule
timeframe dominance rule
symmetry feature definition
deterministic-vs-learnable boundary
```

## Core Hard Rules

```text
X_AXIS = HOOK + NODE_COUNTING
Y_AXIS = RALLY + F_COUNTING
NDS_LOGIC_APPLIES_FRACTALLY_ACROSS_TIMEFRAMES
HIGHER_TIMEFRAME_DOMINATES_LOWER_TIMEFRAME
F2_MUST_BE_GREATER_THAN_OR_EQUAL_TO_F1
HOOK_1_2_3_USUALLY_HAVE_SYMMETRY
HOOK_4_MAY_EXTEND_BEYOND_USUAL_SYMMETRY
```

## Proposed Canonical Objects

```text
NDS_Scale
NDS_Axis
Hook
Rally
Node
F_Count
Cycle
Symmetry
Context
Scenario
Zone
Destination
Invalidation
EntryFamily
ExtremeAnchor
ExecutionIntent
AuditObject
```

## Proposed Datasets

```text
nds_object_model_v1.csv
canonical_state_packet_v1.csv
nds_axis_state_v1.csv
fractal_scale_context_v1.csv
hook_node_counting_state_v1.csv
rally_f_counting_state_v1.csv
symmetry_feature_ledger_v1.csv
timeframe_dominance_ledger_v1.csv
```

## Proposed Fields for `canonical_state_packet_v1`

```text
packet_id
symbol
timestamp
active_timeframe
scale_id
parent_scale_id
child_scale_ids

x_axis_state
x_axis_hook_id
x_axis_node_count_state
x_axis_symmetry_state

y_axis_state
y_axis_rally_id
y_axis_f_count_state
y_axis_symmetry_state

dominant_parent_context_id
parent_dominance_state
context_id
scenario_ids
zone_ids
destination_ids
entry_candidate_ids
invalidation_ids

symmetry_feature_ids
reason_vector_id
audit_object_ids
```

## Proposed Labels

```text
X_AXIS_HOOK_NODE_COUNTING
Y_AXIS_RALLY_F_COUNTING
F2_VALID_EQUAL_OR_LARGER_THAN_F1
F2_INVALID_SMALLER_THAN_F1
HOOK_1_2_3_SYMMETRIC
HOOK_4_EXTENSION_BEYOND_SYMMETRY
PARENT_TIMEFRAME_DOMINANT
CHILD_TIMEFRAME_REFINEMENT
SYMMETRY_SUPPORTS_ZONE
SYMMETRY_SUPPORTS_ENTRY
SYMMETRY_SUPPORTS_EXTREME
```

## Proposed AI Modules

```text
NDS Object Builder
Axis State Builder
Fractal Scale Mapper
Timeframe Dominance Annotator
Symmetry Feature Builder
Symmetry Usefulness Tester
Canonical State Packet Exporter
NDS Object Schema Validator
```

## Architecture Consequence

The system should not feed AI raw candle data as the primary representation.

The system should first construct NDS-native objects:

```text
raw bars
→ NDS axis states
→ Hook/Node objects
→ Rally/F objects
→ Fractal context packet
→ Scenario/Zone/Destination packet
→ Entry candidates
→ ExecutionIntent
```

AI should operate on this packet.

## Open Questions

1. Should X-axis and Y-axis be stored as separate tables or inside one state packet?
2. What exact numeric rule defines Hook 1/2/3 symmetry?
3. What exact numeric rule defines Hook 4 extension beyond symmetry?
4. Should F2 >= F1 be measured by price distance, time, or both?
5. Should F symmetry include both size and duration?
6. How should parent timeframe dominance be scored when parent and child conflict?
7. Should lower timeframe ever veto higher timeframe, or only refine entry?
8. How should scale IDs be generated across symbols and timeframes?
9. Should every Hook, Rally, Node, and F object be drawn on chart?
10. Should symmetry be a hard requirement for some entries or only a scoring feature?
11. Can symmetry define a zone even when no Extreme exists yet?
12. Should symmetry be tested separately for zone precision, entry precision, and reward?
13. Should symmetry features be visible in audit reports?
14. Which fields should be mandatory in `canonical_state_packet_v1` before AI training?
15. Should the first implementation build deterministic NDS objects before any model training?

## Attachment Index

No images were provided for this answer.
