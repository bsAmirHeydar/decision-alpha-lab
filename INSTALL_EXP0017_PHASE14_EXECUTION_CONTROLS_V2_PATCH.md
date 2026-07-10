# Install — EXP0017 Phase14 Execution Controls V2

## Required baseline

- EXP0017 Phase06 Hotfix011 or later signal authority
- EXP0017 Phase14 Raw Execution Backtest V1
- EXP0017 Phase14 Hotfix001

## Install from repository root

```powershell
Expand-Archive `
  -LiteralPath ".\EXP0017_Phase14_Execution_Controls_V2_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\EXP0017_Phase14_Execution_Controls_V2_Patch.zip" `
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

## Default behavior after installation

```text
Trade leg: protected symbol
Enabled CG: cg_3m only
Entry: first tick after closed confirmation candle
Stop: behind confirmation candle
SELL stop spread adjustment: enabled
Target: ATR(14) × 1.0
Volume model: fixed monetary risk
Fixed risk amount: 100 account-currency units
Hedging: enabled
Execution drawings: enabled
Runtime: Strategy Tester only
```

## Verification

```powershell
python -m pytest -q research/exp0017_phase14/tests/test_phase14_raw_execution_contract.py
python tools/engineering/validate_alpha_lab_policy.py
python tools/engineering/check_mql5_compatibility.py
python tools/engineering/audit_repository_layout.py
```

## Stage and commit

```powershell
git add -- `
  "INSTALL_EXP0017_PHASE14_EXECUTION_CONTROLS_V2_PATCH.md" `
  "EXP0017_PHASE14_EXECUTION_CONTROLS_V2_MANIFEST.json" `
  "mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Raw_Execution_Backtest.mq5" `
  "mql5/Experts/IntermarketDivergenceExecution/README.md" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Types.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Utilities.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_StopModel.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_TargetModelATR.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_TargetModelRiskMultiple.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_TargetModel.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_VolumeModel.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_TradePlanner.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_OrderRouter.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Audit.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_ExecutionVisuals.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Engine.mqh" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_INDEX.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_EXECUTION_CONTRACT.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_MODULE_ARCHITECTURE.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_BACKTEST_OPERATOR_GUIDE.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_VALIDATION_PLAN.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_EXECUTION_CONTROLS_V2.md" `
  "research/exp0017_phase14/tests/test_phase14_raw_execution_contract.py"

git status
git diff --cached --stat

git commit `
  -m "feat(exp0017): add hedge risk target and execution visual controls" `
  -m "Add input-controlled hedging, spread-adjusted sell stops, ATR and stop-risk-multiple targets, strict fixed-money risk sizing with maximum broker-valid volume below the risk cap, and optional drawings for accepted CG executions."

git push
```

## Rollback

Restore the listed files from the previous commit and remove these new modules:

```text
CGX_TargetModelRiskMultiple.mqh
CGX_TargetModel.mqh
CGX_ExecutionVisuals.mqh
PHASE14_EXECUTION_CONTROLS_V2.md
```
