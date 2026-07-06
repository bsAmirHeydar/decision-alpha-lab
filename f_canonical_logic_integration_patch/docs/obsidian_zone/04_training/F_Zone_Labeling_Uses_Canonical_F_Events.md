# F-Zone Labeling Uses Canonical F Events

Training labels for F-derived zones must be built from canonical F events, not from visual approximations.

## Label Source

A training sample may use F1/F2/F3 fields only when those fields come from:

- Phoenix canonical event output;
- audit-equivalent exported canonical sequence data;
- a documented extraction path that matches the canonical F-counting contract.

## Prohibited

Do not label a sample as `f2_waist_branch_zone` merely because the chart visually looks like F2.

## Correct Label Example

```yaml
zone_source: F2_WAIST_BREAK_BRANCH
f_event_id: <canonical_f2_event_id>
f_lifecycle_state: confirmed_or_branch_active
point_1_source: F2_WAIST
point_2_source: NODE_THAT_PASSES_F2_WAIST
execution_permission: child_zone_required_if_stop_unstable
```
