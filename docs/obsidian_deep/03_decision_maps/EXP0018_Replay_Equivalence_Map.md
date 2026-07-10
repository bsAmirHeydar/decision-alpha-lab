  ---
  id: EXP0018_Replay_Equivalence_Map
  title: "EXP0018 Replay Equivalence Map"
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
# EXP0018 Replay Equivalence Map

```mermaid
flowchart LR
 Hist[Historical Cursor]-->Engine[Same Core Engine]
 Live[Closed-Bar Feed]-->Engine
 Engine-->EH[Event Hashes]
 EH-->Compare{Equal?}
 Compare--yes-->Pass[Parity]
 Compare--no-->Trace[First Causal Mismatch]
```
