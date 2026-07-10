  ---
  id: EXP0018_Core_Phase_Gate_Map
  title: "EXP0018 Core Phase Gate Map"
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
# EXP0018 Core Phase Gate Map

```mermaid
flowchart LR
 Ready[DoR]-->Design[Contract+Fixtures]
 Design-->Patch[Bounded Patch]
 Patch-->Compile[Compile]
 Compile-->Replay[Replay/Visual]
 Replay-->Evidence[Evidence Package]
 Evidence-->Done[DoD]
```
