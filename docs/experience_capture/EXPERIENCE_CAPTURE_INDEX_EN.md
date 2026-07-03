# Experience Capture Index

## Captured Records

### EXT-06 — Node Penetration and Extreme Invalidation

Path:

```text
docs/experience_capture/answers/EXT-06/
```

Summary:

For an Extreme anchor based on a cycle-origin node, any penetration beyond the node, even by one point, ends the validity of that node. Quick return does not preserve the original node. The old Extreme is structurally dead, although the penetration-then-reversal event should be recorded for execution and policy learning.

Main derived architecture requirements:

```text
node_penetration_ledger_v1.csv
extreme_invalidation_ledger_v1.csv
penetration_then_reversal_ledger_v1.csv
stop_hit_then_reverse_ledger_v1.csv
EXTREME_NODE_VALIDITY_GATE
```
