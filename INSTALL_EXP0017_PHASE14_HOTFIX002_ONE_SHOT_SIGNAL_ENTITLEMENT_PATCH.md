# Install — EXP0017 Phase14 Hotfix002 One-Shot Signal Entitlement

## Required baseline

- EXP0017 Phase06 Hotfix011 or later signal authority
- EXP0017 Phase14 Raw Execution Backtest V1
- EXP0017 Phase14 Hotfix001
- EXP0017 Phase14 Execution Controls V2

## Install from repository root

```powershell
Expand-Archive `
  -LiteralPath ".\EXP0017_Phase14_Hotfix002_OneShot_Signal_Entitlement_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\EXP0017_Phase14_Hotfix002_OneShot_Signal_Entitlement_Patch.zip" `
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

## Hard behavior after installation

```text
One divergence anatomy = one non-retryable execution entitlement.
Repeated detection on later lower-timeframe candles = suppressed.
Planner rejection = entitlement remains consumed.
Position-policy rejection = entitlement remains consumed.
Broker rejection = entitlement remains consumed.
Successful order = entitlement remains consumed.
Same-day restart = warmup reconstructs consumed entitlements.
```

This policy is not exposed as an input and cannot be disabled accidentally.

## Audit files

```text
Main: EXP0017_Phase14_Raw_Execution_Audit_V3.csv
Gate: EXP0017_Phase14_Raw_Execution_Audit_V3_OneShot_Gate.csv
```

## Verification

```powershell
python -m pytest -q research/exp0017_phase14/tests/test_phase14_raw_execution_contract.py
python tools/engineering/validate_alpha_lab_policy.py
python tools/engineering/check_mql5_compatibility.py
python tools/engineering/audit_repository_layout.py
python docs/ai_algorithm_engineering_os/tools/validate_vault.py
```

## Stage and commit

```powershell
git add -- `
  "INSTALL_EXP0017_PHASE14_HOTFIX002_ONE_SHOT_SIGNAL_ENTITLEMENT_PATCH.md" `
  "EXP0017_PHASE14_HOTFIX002_ONE_SHOT_SIGNAL_ENTITLEMENT_MANIFEST.json" `
  "mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Raw_Execution_Backtest.mq5" `
  "mql5/Experts/IntermarketDivergenceExecution/README.md" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Types.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Utilities.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_TradeEntitlement.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_SignalRegistry.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_TradePlanner.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_OrderRouter.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Audit.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/Execution/CGX_Engine.mqh" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/README.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/06_execution_and_risk_contract.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_INDEX.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_EXECUTION_CONTRACT.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_MODULE_ARCHITECTURE.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_BACKTEST_OPERATOR_GUIDE.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_VALIDATION_PLAN.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_EXECUTION_CONTROLS_V2.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_ONE_SHOT_SIGNAL_EXECUTION_CONTRACT.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_ONE_SHOT_STATE_MACHINE.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/PHASE14_ONE_SHOT_VALIDATION_PLAN.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase14_raw_execution_backtest/hotfixes/PHASE14_HOTFIX_002_ONE_SHOT_SIGNAL_ENTITLEMENT.md" `
  "research/exp0017_phase14/tests/test_phase14_raw_execution_contract.py"

git status
git diff --cached --stat

git commit `
  -m "fix(exp0017): enforce one-shot divergence execution entitlement" `
  -m "Assign each divergence anatomy a canonical symbol-order-invariant trade entitlement, consume it before planning and routing, suppress all later lower-candle observations, reconstruct consumed state during startup warmup, and document and audit the non-retryable execution contract."

git push
```
