# INSTALL — EXP0017 Phase 06 Hotfix003 Dual-Symbol Full Visual Language

This patch upgrades Phase 06 so divergence drawings are created on both input-symbol charts at the same time.

## Install

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-phase06-hotfix003-dual-symbol-full-visual-language-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-phase06-hotfix003-dual-symbol-full-visual-language-patch.zip"
```

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

## Important defaults

- `InpShowChartPanel = false`
- `InpDrawOnBothInputSymbolCharts = true`
- `InpOpenMissingInputSymbolCharts = true`
- all visual drawing components are enabled by default
- ledger remains enabled
- no orders, no risk, no targets, no performance statistics, no AI
