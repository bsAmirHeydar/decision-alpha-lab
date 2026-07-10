  ---
  id: EXP0018_Reference_Lifecycle_Design_Map
  title: "EXP0018 Reference Lifecycle Design Map"
  type: decision-map
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- decision-map
- implementation-design
  ---
# EXP0018 Reference Lifecycle Design Map

```mermaid
stateDiagram-v2
 [*] --> Candidate
 Candidate --> Active
 Active --> Protected
 Protected --> Consumed: protected hunts
 Protected --> Retired: policy retirement
 Consumed --> Retired
 Retired --> [*]
```
