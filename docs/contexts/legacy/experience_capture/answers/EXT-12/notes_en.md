# EXT-12 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
ontology separation rule
classical support/resistance rejection rule
cycle-view definition
node-view definition
NDS translation requirement
```

## Main Design Consequence

The system must prevent classical support/resistance from entering as a native concept.

Extreme must be represented as an NDS-native object, not a support/resistance level.

## Proposed Hard Rules

```text
EXTREME_IS_NOT_SUPPORT_RESISTANCE
SUPPORT_RESISTANCE_NATIVE_TERMS_FORBIDDEN
CLASSICAL_LEVEL_LOGIC_REJECTED_UNLESS_TRANSLATED_TO_NDS
EXTREME_REQUIRES_CYCLE_VIEW
EXTREME_REQUIRES_NODE_VIEW
```

## Proposed Translation Rule

If a concept looks like support/resistance, it must be translated into:

```text
node logic
cycle state
near-death zone
scenario region
destination
invalidation
```

If it cannot be translated, it must be rejected.

## Proposed Datasets

```text
extreme_vs_support_resistance_boundary_v1.csv
nds_level_translation_ledger_v1.csv
ontology_contamination_checks_v1.csv
cycle_node_extreme_definition_v1.csv
```

## Proposed Fields

```text
extreme_id
anchor_node_id
node_level
cycle_origin_node_id
cycle_state
near_death_zone_present
stop_behind_node
node_penetration_invalidation
context_valid
zone_valid
scenario_alive
classical_sr_term_detected
nds_translation_available
ontology_gate_result
```

## Proposed Labels

```text
NDS_EXTREME
CLASSICAL_SR_REJECTED
SR_TRANSLATED_TO_NODE_LOGIC
ONTOLOGY_CONTAMINATION_RISK
CYCLE_VIEW_PRESENT
NODE_VIEW_PRESENT
NEAR_DEATH_LOGIC_PRESENT
STOP_BEHIND_NODE_PRESENT
```

## Proposed AI Modules

```text
NDS Level Ontology Gate
Support/Resistance Contamination Checker
Cycle-Node Extreme Validator
NDS Translation Validator
Extreme Object Schema Validator
```

## Open Questions

1. Should the term support/resistance be banned completely from docs, or allowed only in contrast sections?
2. Should the system automatically reject feature names containing support/resistance?
3. Can old support/resistance screenshots be used only if relabeled into NDS node/cycle language?
4. What exact NDS fields must be present before a level can be called Extreme?
5. Is L2 required for the distinction, or is the deeper distinction the cycle/node view?
6. Should near-death logic be required for every Extreme record?
7. Should stop-behind-node be mandatory for the Extreme object schema?
8. Can a node act like a classical level but still be valid if it is fully NDS-defined?
9. Should ontology contamination checks run before every dataset export?
10. Should the model report any support/resistance-like learned rule as rejected until translated?
11. Should destination and invalidation be required to separate Extreme from vague level trading?
12. Should multi-scenario context be required before an Extreme can be accepted?
13. Should fractal context be mandatory for every Extreme candidate?
14. Can the first implementation use a rule-based ontology gate before AI?
15. Should the NDS glossary explicitly include a section called "Not Support/Resistance"?

## Attachment Index

No images were provided for this answer.
