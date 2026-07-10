# Install — EXP0017 Phase14 Raw Execution Backtest V1

## Scope

This root-relative patch adds the first modular order-producing EXP0017 expert.

Required baseline:

```text
EXP0017 Phase06 Hotfix011 — NDX Raw-Path Freshness Authority
```

## Install from repository root

Place the ZIP in the project root, then run:

```powershell
Expand-Archive `
  -LiteralPath ".\EXP0017_Phase14_Raw_Execution_Backtest_V1_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\EXP0017_Phase14_Raw_Execution_Backtest_V1_Patch.zip" `
  -Force
```

## Compile

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Raw_Execution_Backtest.mq5
```

Required MetaEditor result:

```text
0 errors, 0 warnings
```

## Default profile

```text
runtime               = BACKTEST_ONLY
trade leg             = PROTECTED_SYMBOL
entry                  = market after closed confirmation candle
stop                   = behind selected symbol confirmation candle
ATR period             = 14
ATR multiplier         = 1.0
volume                 = 1% equity risk
hedging account        = required
cg_3m                  = enabled
all other CGs          = disabled
```

## Automated checks executed for this patch

```text
Phase14 contract tests:       8 passed
MQL5 compatibility scan:     0 errors, 0 warnings
Engineering policy:          0 errors, 0 warnings
Repository layout audit:     0 missing directories
AI Engineering OS vault:     0 errors, 0 warnings
Brace/include preflight:     passed
```

MetaEditor compilation and Strategy Tester execution must still be performed on the target terminal.

## Stage and commit

```powershell
git add -- `
  "INSTALL_EXP0017_PHASE14_RAW_EXECUTION_BACKTEST_V1_PATCH.md" `
  "EXP0017_PHASE14_RAW_EXECUTION_BACKTEST_V1_MANIFEST.json" `
  "mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Raw_Execution_Backtest.mq5" `
  "mql5/Experts/IntermarketDivergenceExecution/README.md" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Types.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Utilities.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_SignalSource.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_ClosedCandle.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_EntryModel.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_StopModel.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_TargetModelATR.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_VolumeModel.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_TradePlanner.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_SignalRegistry.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_OrderRouter.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Audit.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Engine.mqh" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/README.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/06_execution_and_risk_contract.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/07_mql5_modular_architecture.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_INDEX.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_EXECUTION_CONTRACT.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_MODULE_ARCHITECTURE.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_BACKTEST_OPERATOR_GUIDE.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_VALIDATION_PLAN.md" `
  "research/exp0017_phase14/tests/test_phase14_raw_execution_contract.py"

git diff --cached --stat

git commit `
  -m "feat(exp0017): add modular CG raw execution backtest" `
  -m "Execute confirmed cycle-group divergences on closed candles with selectable protected or hunter leg, confirmation-candle stops, ATR targets, risk-normalized volume, deterministic signal deduplication, dual-symbol lifecycle warmup, tester-only transport by default, and CG3 as the sole enabled default profile."

git push
```

## Rollback

Revert the commit. No migration is required. The patch does not modify the Hotfix011 signal-anatomy source files.
