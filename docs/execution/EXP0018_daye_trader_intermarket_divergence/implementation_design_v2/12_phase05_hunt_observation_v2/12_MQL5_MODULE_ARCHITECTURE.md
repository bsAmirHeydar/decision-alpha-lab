---
id: EXP0018-P05-MQL5
title: "P05 MQL5 Module Architecture"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Modules

- `DAYE_HuntTypes.mqh` — domain schema and enums
- `DAYE_HuntClassifier.mqh` — pure touch classification
- `DAYE_HuntStore.mqh` — bounded read-only observation store
- `DAYE_HuntEvents.mqh` — state transition detection
- `DAYE_HuntDiagnostics.mqh` — human-readable diagnostics
- `DAYE_HuntAudit.mqh` — optional CSV adapter
- `DAYE_HuntSelfTest.mqh` — embedded deterministic tests
- `DAYE_HuntEngine.mqh` — runtime owner and P04 dependency orchestration
- `EXP0018_Daye_Hunt_Observation_Anatomy.mq5` — input and timer shell

Detection, persistence, diagnostics, and orchestration remain separate.
