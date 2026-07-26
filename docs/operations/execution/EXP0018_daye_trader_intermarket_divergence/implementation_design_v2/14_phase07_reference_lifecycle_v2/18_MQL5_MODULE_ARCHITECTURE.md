# MQL5 module architecture

- `DAYE_LifecycleTypes.mqh` — schemas and enums;
- `DAYE_LifecycleIdentity.mqh` — deterministic IDs;
- `DAYE_LifecycleStore.mqh` — bounded state store;
- `DAYE_LifecycleStateMachine.mqh` — pure transition logic;
- `DAYE_LifecycleEvents.mqh` — typed event creation;
- `DAYE_LifecycleCheckpoint.mqh` — restart persistence;
- `DAYE_LifecycleDiagnostics.mqh` — formatting;
- `DAYE_LifecycleAudit.mqh` — CSV adapter;
- `DAYE_LifecycleSelfTest.mqh` — embedded contract tests;
- `DAYE_LifecycleEngine.mqh` — state owner and orchestration;
- `EXP0018_Daye_Reference_Lifecycle_Anatomy.mq5` — inputs and timer lifecycle.
