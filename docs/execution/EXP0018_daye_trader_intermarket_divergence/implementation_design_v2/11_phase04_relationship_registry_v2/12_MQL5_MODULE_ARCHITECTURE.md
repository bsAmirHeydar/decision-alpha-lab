---
id: EXP0018-P04-MQL5-ARCH
title: "P04 MQL5 Module Architecture"
type: architecture
status: active
project: EXP0018
phase: P04
---
# MQL5 Module Architecture

```text
DAYE_RelationshipTypes
  → DAYE_RelationshipRegistry
  → DAYE_RelationshipResolver
  → DAYE_RelationshipStore
  → DAYE_RelationshipEvents
  → DAYE_RelationshipDiagnostics
  → DAYE_RelationshipAudit
  → DAYE_RelationshipSelfTest
  → DAYE_RelationshipEngine
  → EXP0018_Daye_Relationship_Registry_Anatomy
```

P03 receives a read-only export surface (`GetCurrentSummary`, `ExportPeriods`). P04 does not mutate P03 period snapshots.
