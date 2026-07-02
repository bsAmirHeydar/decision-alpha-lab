# BASE-03 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
reason ontology principle
reason_vector design input
signal framework design input
entry-family expansion requirement
```

## Main Design Consequence

The system must distinguish between:

```text
valid anatomy-native reasons
non-anatomy noise
```

The model should not consume arbitrary chart features.

It should consume only reasons grounded in:

```text
Hook state
Rally state
fractal relation
execution geometry
```

## Suggested Reason Categories

### Structural reasons

```text
hook_number
hook_state
hook_late_state
hook_3_proximity
hook_4_proximity
second_hook_rally_proneness
rally_f_index
rally_terminal_state
```

### Fractal reasons

```text
higher_tf_direction
higher_tf_hook_state
higher_tf_rally_state
higher_tf_f_state
lower_tf_entry_pattern
parent_child_alignment
parent_child_conflict
```

### Execution reasons

```text
entry_framework_type
entry_geometry_ready
stop_geometry_ready
target_geometry_ready
flag_waist_reference_ready
extreme_reference_ready
```

## Suggested Signal Framework Library

The answer implies a future library of entry families.

Initial candidates:

```text
HOOK_HOOK_RALLY
HIGHER_TF_F3__LOWER_TF_3F_REVERSAL
POST_F1_DIRECTIONAL_CONTINUATION
EXTREME_ENTRY
```

This list is not final and should expand over time.

## Proposed Dataset Consequence

The future system may need:

```text
reason_vector_v1
signal_framework_ledger_v1
entry_family_catalog_v1
```

## Proposed AI Modules

```text
Reason Vector Builder
Signal Framework Classifier
Entry Family Selector
Reason Quality Gate
Noise Rejection Gate
```

## Open Questions

1. Exactly what makes Hook 2 prone to Rally when Hook 1 remains unhit?
2. What are all valid Hook-Hook-Rally variants?
3. How many different entry families should the first catalog contain?
4. What exactly qualifies a lower-timeframe 3-F reversal inside a higher-timeframe F3?
5. What are the full rules for post-F1 continuation entry?
6. What other anatomy-native signal frameworks exist beyond the ones already named?
7. When two different entry families are both valid, should they be ranked or both kept alive?
8. Should the reason_vector store raw state facts or also derived conclusions?
9. Should noise be explicitly tagged, or simply omitted?
10. Can some currently rejected features ever be accepted if translated into anatomy-native language?

## Attachment Index

```text
images/BASE-03-image-01-hook-hook-rally-example.png
```
