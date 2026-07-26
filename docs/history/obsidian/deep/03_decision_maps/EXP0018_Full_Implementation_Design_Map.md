  ---
  id: EXP0018_Full_Implementation_Design_Map
  title: "EXP0018 Full Implementation Design Map"
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
# EXP0018 Full Implementation Design Map

```mermaid
flowchart TD
 S[Sources]-->D[Doctrine Freeze]
 D-->T[Time]
 T-->DS[Data Sync]
 DS-->P[Periods]
 P-->R[22 Registry]
 R-->H[Hunt]
 H-->C[Close Confirmation]
 C-->L[Lifecycle]
 L-->V[Visual]
 V-->RP[Replay]
 RP-->QA[Core RC]
 QA-->O[Optional Research]
```
