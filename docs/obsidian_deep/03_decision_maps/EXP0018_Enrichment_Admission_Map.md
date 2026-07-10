  ---
  id: EXP0018_Enrichment_Admission_Map
  title: "EXP0018 Enrichment Admission Map"
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
# EXP0018 Enrichment Admission Map

```mermaid
flowchart TD
 Claim[PDF Claim]-->Class{Status}
 Class-- conflict/quarantined -->Stop[No Code Path]
 Class-- research candidate -->ADR[Admission ADR]
 ADR-->Ledger[Ledger-only Module]
 Ledger-->OOS[Outcome/OOS]
 OOS-->Human[Architect Promotion]
```
