  ---
  id: EXP0018_Source_Claim_Promotion_Map
  title: "EXP0018 Source Claim Promotion Map"
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
# EXP0018 Source Claim Promotion Map

```mermaid
flowchart TD
 Source-->Claim
 Claim-->Authority
 Authority-->Decision
 Decision-->ADR
 ADR-->Rule
 Rule-->Fixture
 Fixture-->Code
```
