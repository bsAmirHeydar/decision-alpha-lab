# Install EXP0017 Phase06 Hotfix007 Protected Reference Retirement Patch

This patch prevents retired reference sides from producing repeated divergence drawings after the protected/clean symbol has hunted its own reference.

## Install

Expand the patch at the repository root and compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

## Important inputs

```text
InpEnableProtectedReferenceRetirement = true
InpRetireReferenceWhenProtectedHunts = true
InpAllowRepeatedDivergenceWhileProtectedSurvives = true
InpSuppressRetiredReferenceSignals = true
```
