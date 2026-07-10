# Install — EXP0017 Phase 06 Hotfix010

## Patch purpose

This patch fixes the remaining non-host `NDXUSD` freshness asymmetry in both signal logic and chart rendering.

## Installation

Place the ZIP in the repository root, then run:

```powershell
Expand-Archive `
  -LiteralPath ".\EXP0017_Phase06_Hotfix010_DualSymbol_M1_Evidence_Parity_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\EXP0017_Phase06_Hotfix010_DualSymbol_M1_Evidence_Parity_Patch.zip" `
  -Force
```

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

Then remove the old expert instance and attach version `1.10` only to `SPXUSD`. Keep the `NDXUSD` chart open without another instance.

## Expected first-run behavior

If NDX M1 history is still loading, the journal can show:

```text
EXP0017 Phase06 Hotfix010: historical backfill waiting for complete M1 coverage on both configured symbols.
```

This is intentional. Backfill retries automatically and does not finalize a partial NDX reconstruction.

## Required validation inputs

```text
InpRequireM1History = true
InpEnableExtremeFrontierReferenceFilter = true
InpRequireSymbolLocalFrontierForBothSymbols = true
InpSuppressNonFrontierReferenceSignals = true
InpEnableHistoricalVisualBackfill = true
InpClearPhase06ObjectsOnInit = true
InpDrawOnBothInputSymbolCharts = true
```

## Commit

```powershell
git add -- `
  "INSTALL_EXP0017_PHASE06_HOTFIX010_DUAL_SYMBOL_M1_EVIDENCE_PARITY_PATCH.md" `
  "EXP0017_PHASE06_HOTFIX010_MANIFEST.json" `
  "mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5" `
  "mql5/Include/IntermarketDivergenceExecution/CG/CGR_ReferenceField.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/CGH_HuntField.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/CGC_Types.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/CGC_ConfirmationField.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/CGV_Drawing.mqh" `
  "mql5/Include/IntermarketDivergenceExecution/CG/CGV_Engine.mqh" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase06_visual_ledger_anatomy/PHASE06_INDEX.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase06_visual_ledger_anatomy/hotfixes/PHASE06_HOTFIX_010_DUAL_SYMBOL_M1_EVIDENCE_PARITY.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase06_visual_ledger_anatomy/hotfixes/PHASE06_HOTFIX_010_LOGIC_AND_RENDER_CONTRACT.md" `
  "docs/execution/EXP0017_cycle_group_intermarket_divergence/phase06_visual_ledger_anatomy/hotfixes/PHASE06_HOTFIX_010_VALIDATION_PLAN.md"

git diff --cached --stat

git commit `
  -m "fix(exp0017): enforce dual-symbol M1 evidence parity" `
  -m "Reject partial non-host M1 intervals, treat missing later cycles as frontier barriers, retry backfill until both symbols are ready, and align drawing anchors with exclusive signal boundaries."

git push
```
