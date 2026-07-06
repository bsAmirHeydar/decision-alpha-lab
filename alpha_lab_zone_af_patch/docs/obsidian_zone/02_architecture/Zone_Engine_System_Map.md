---
type: architecture_map
id: ZONE-ENGINE-SYSTEM-MAP
status: draft
language: english
---

# Zone Engine System Map

```text
Mechanical Context
  -> Movement Constraint
  -> Approximate Reversal Area
  -> Zone Candidate
  -> Stability Classification
      -> Execution Zone
      -> Watch Zone
      -> Context Zone
      -> Unsafe No-Stop Area
  -> Parent/Child Refinement
  -> Limit Order Plan
  -> Touch Event
  -> Outcome Label
  -> Ranking / Learning Loop
```

## Source Families

- [[../01_concepts/Hook_Zone|Hook Zone]]
- [[../01_concepts/F1_Zone|F1 Zone]]
- [[../01_concepts/F2_Zone|F2 Zone]]
- [[../01_concepts/F3_Zone|F3 Zone]]

## Core Policies

- [[../03_policies/No_Stop_No_Trade|No Stop, No Trade]]
- [[../03_policies/Wide_Zone_Requires_Child_Zone|Wide Zone Requires Child Zone]]
- [[../03_policies/No_Fake_Pattern_Policy|No Fake Pattern Policy]]

