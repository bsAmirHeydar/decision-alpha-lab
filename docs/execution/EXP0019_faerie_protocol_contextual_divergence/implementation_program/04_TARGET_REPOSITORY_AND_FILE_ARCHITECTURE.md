---
title: "Target Repository and File Architecture"
tags: [exp0019, faerie-protocol, implementation-program, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Target Repository and File Architecture

## Canonical target layout

```text
mql5/
├── Include/
│   └── IntermarketDivergenceContexts/
│       └── EXP0019_FaerieProtocol/
│           ├── FP_All.mqh
│           ├── FP_Enums.mqh
│           ├── FP_Types.mqh
│           ├── FP_Config.mqh
│           ├── FP_Identity.mqh
│           ├── FP_ReasonCodes.mqh
│           ├── FP_TimeAdapter.mqh
│           ├── FP_SessionCalendar.mqh
│           ├── FP_WeekCalendar.mqh
│           ├── FP_SymbolPair.mqh
│           ├── FP_M1Synchronizer.mqh
│           ├── FP_DataCoverage.mqh
│           ├── FP_WindowStore.mqh
│           ├── FP_ReferenceEngine.mqh
│           ├── FP_RelationRegistry.mqh
│           ├── FP_HuntAdapter.mqh
│           ├── FP_CandidateEngine.mqh
│           ├── FP_ConfirmationEngine.mqh
│           ├── FP_WWEngine.mqh
│           ├── FP_LifecycleEngine.mqh
│           ├── FP_SignalLedger.mqh
│           ├── FP_QuotaArbiter.mqh
│           ├── FP_RiskAdapter.mqh
│           ├── FP_IndicatorProjection.mqh
│           ├── FP_IndicatorObjectManager.mqh
│           ├── FP_IndicatorPanel.mqh
│           ├── FP_AlertRouter.mqh
│           ├── FP_AuditExporter.mqh
│           ├── FP_Diagnostics.mqh
│           ├── FP_Checkpoint.mqh
│           └── FP_Engine.mqh
├── Indicators/
│   └── FaerieProtocol/
│       └── EXP0019_FaerieProtocol_Context.mq5
├── Experts/
│   └── FaerieProtocol/
│       ├── EXP0019_FaerieProtocol_Diagnostic.mq5
│       ├── EXP0019_FaerieProtocol_Paper.mq5
│       └── EXP0019_FaerieProtocol_Live.mq5
└── Experts/
    └── FaerieProtocolTests/
        ├── EXP0019_FP_Time_SelfTest.mq5
        ├── EXP0019_FP_Data_SelfTest.mq5
        ├── EXP0019_FP_Relation_SelfTest.mq5
        ├── EXP0019_FP_WW_SelfTest.mq5
        ├── EXP0019_FP_Indicator_SelfTest.mq5
        ├── EXP0019_FP_Replay_Parity.mq5
        └── EXP0019_FP_PaperExecution_SelfTest.mq5
```

## Ownership rules

| Layer | Owns | Must not own |
|---|---|---|
| Shared core | generic time/reference/hunt/divergence/identity primitives | FP relation policy |
| FP context | sessions, relations, lifecycle, WW, suppression, quota eligibility | chart objects or broker API |
| Indicator projection | rendering, panel, alerts, exports | detection truth or execution |
| Diagnostic EA | replay, differential traces, health | orders |
| Paper EA | synthetic order lifecycle | broker orders |
| Live EA | authorized broker adapter only | alternate detector |

## Dependency direction

Dependencies point inward toward contracts and cores. `FP_Engine.mqh` composes modules; leaf modules never include the indicator or EA entry points. Visual modules consume immutable snapshots and events rather than calling detection logic.

## File-size and responsibility limits

- Entry-point `.mq5` files should remain orchestration shells.
- A module with more than one state machine must be split.
- A file that imports trade APIs cannot be imported by indicator or core modules.
- A visual object manager may create/delete/update objects but may not decide signal state.
