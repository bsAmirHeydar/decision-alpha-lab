---
id: EXP0018-P02-MQL5-ARCH
title: "P02 MQL5 Module Architecture"
type: architecture
status: active
project: EXP0018
---
# معماری MQL5

```text
DAYE_DataTypes
  ↓
DAYE_SymbolContract
  ↓
DAYE_DataQuality
  ↓
DAYE_DataSynchronizer
  ↓
DAYE_DataEvents
  ↓
DAYE_DataDiagnostics / DAYE_DataAudit
  ↓
DAYE_DataEngine
  ↓
EXP0018_Daye_Data_Sync_Anatomy
```

Pure alignment در synchronizer است. File I/O در audit adapter است. Mutable runtime state فقط در engine نگه‌داری می‌شود.
