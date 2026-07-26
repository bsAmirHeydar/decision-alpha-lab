# Phase 03 Index — Hunt Anatomy

Phase 03 adds the first price-action interpretation layer to EXP0017.

It does not build divergence, confirmation, invalidation, entries, exits, risk, targets, reports, ranking, or AI behavior.

Its only responsibility is to answer this question for every enabled Cycle Group, every completed previous same-day reference cycle, and both symbols:

```text
Did the current cycle touch or break the reference high or reference low?
```

## Added MQL5 files

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Hunt_Anatomy.mq5
mql5/Include/IntermarketDivergenceExecution/CG/CGH_Types.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGH_HuntField.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGH_Display.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGH_Engine.mqh
```

## Documentation set

- [[PHASE03_HUNT_ANATOMY_SPEC]]
- [[PHASE03_MQL5_MODULE_ARCHITECTURE]]
- [[PHASE03_HUNT_DATA_CONTRACT]]
- [[PHASE03_VALIDATION_AND_TEST_PLAN]]
- [[PHASE03_LIMITS_AND_NON_GOALS]]
- [[PHASE03_HANDOFF_TO_PHASE04]]
- [[PHASE03_OBSIDIAN_GUIDE]]
