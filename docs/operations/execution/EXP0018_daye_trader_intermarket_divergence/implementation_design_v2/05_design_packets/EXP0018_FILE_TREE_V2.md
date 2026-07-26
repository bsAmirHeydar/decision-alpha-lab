  ---
  id: EXP0018-FILE-TREE-V2
  title: "EXP0018 Proposed File Tree v2"
  type: architecture
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---

# درخت فایل پیشنهادی

```text
mql5/Experts/DayeTrader/
  EXP0018_Daye_Time_Foundation.mq5
  EXP0018_Daye_Data_Sync_Anatomy.mq5
  EXP0018_Daye_Period_Anatomy.mq5
  EXP0018_Daye_Hunt_Anatomy.mq5
  EXP0018_Daye_Confirmation_Anatomy.mq5
  EXP0018_Daye_Lifecycle_Anatomy.mq5
  EXP0018_Daye_Visual_Anatomy.mq5
  EXP0018_Daye_Replay_Anatomy.mq5
  EXP0018_Daye_Core_RC.mq5

mql5/Include/DayeTrader/EXP0018/
  DAYE_Types.mqh
  DAYE_Time.mqh
  DAYE_DataSynchronizer.mqh
  DAYE_PeriodStore.mqh
  DAYE_SignalRegistry.mqh
  DAYE_HuntDetector.mqh
  DAYE_ConfirmationStateMachine.mqh
  DAYE_ReferenceLifecycleStore.mqh
  DAYE_VisualEvent.mqh
  DAYE_Drawing.mqh
  DAYE_SessionBoxRenderer.mqh
  DAYE_TwoTdoResolver.mqh
  DAYE_ReplayEngine.mqh
  DAYE_AuditLedger.mqh
  Optional/
    DAYE_ExtendedOpenRegistry.mqh
    DAYE_DfrEngine.mqh
    DAYE_SsmtEngine.mqh
    DAYE_ContextLedger.mqh
    DAYE_EventCalendarAdapter.mqh
    DAYE_TriadObserver.mqh
```

هر Phase فقط فایل‌های مالک خود را تغییر می‌دهد. Refactor cross-phase نیازمند ADR جدا است.
