# Install — EXP0017 Phase14 Hotfix001 Signal Source Direct Dependency

## Required baseline

`EXP0017 Phase14 Raw Execution Backtest V1`

## Install from repository root

```powershell
Expand-Archive `
  -LiteralPath ".\EXP0017_Phase14_Hotfix001_SignalSource_Direct_Dependency_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\EXP0017_Phase14_Hotfix001_SignalSource_Direct_Dependency_Patch.zip" `
  -Force
```

## Compile

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Raw_Execution_Backtest.mq5
```

Required result:

```text
0 errors, 0 warnings
```
