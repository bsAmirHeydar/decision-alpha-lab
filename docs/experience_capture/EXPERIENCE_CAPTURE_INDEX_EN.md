# Experience Capture Index

## Captured Records

### NDS-R02 — CycleHook Lifecycle and Sequence Model

Path:

```text
docs/experience_capture/answers/NDS-R02/
```

Summary:

Hook and Cycle are the same algorithmic object in NDS. A CycleHook starts from a valid node, moves toward an opposite Extreme, and later returns toward the origin into ND. Positive CycleHooks count descending valleys; negative CycleHooks count ascending peaks. Each CycleHook contains multiple sequences, each with local numbering and X/Y readings. L starts at 2 and increases until sequence node count is four or less, with separate fixed-origin and recalculated-origin views. Closure requires a sequence reaching three or four nodes plus more than 50% return toward the origin; symmetry is not required but helps project reversal zones and refine entries. Hook types A/B/C classify the broader structure, while X/Y closure scores internal sequence strength.

Main derived architecture requirements:

```text
cyclehook_lifecycle_state_model_v1.csv
hook_sequence_model_v1.csv
x_sequence_y_sequence_model_v1.csv
adaptive_l_coefficient_policy_v1.csv
hook_type_abc_classifier_v1.csv
symmetry_projection_model_v1.csv
nd_threshold_policy_v1.csv
```
