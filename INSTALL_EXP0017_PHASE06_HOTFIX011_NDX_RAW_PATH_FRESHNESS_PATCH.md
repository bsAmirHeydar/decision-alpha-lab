# Install — EXP0017 Phase06 Hotfix011 NDX Raw-Path Freshness

## Preconditions

- Apply this patch from the repository root.
- Hotfix010 must already be present.
- Close MetaEditor files or allow overwrite.

## Install

```powershell
Expand-Archive `
  -LiteralPath ".\EXP0017_Phase06_Hotfix011_NDX_Raw_Path_Freshness_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\EXP0017_Phase06_Hotfix011_NDX_Raw_Path_Freshness_Patch.zip" `
  -Force
```

## Compile

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

Required result:

```text
0 errors, 0 warnings
```

## Runtime reset

1. Remove the old EA instance from SPXUSD.
2. Keep SPXUSD and NDXUSD charts open.
3. Attach version 1.11 only to SPXUSD.
4. Keep `InpClearPhase06ObjectsOnInit=true` for the first run.
5. Do not attach a second instance to NDXUSD.

## Required inputs

```text
InpRequireM1History = true
InpEnableExtremeFrontierReferenceFilter = true
InpRequireSymbolLocalFrontierForBothSymbols = true
InpSuppressNonFrontierReferenceSignals = true
InpDrawOnBothInputSymbolCharts = true
InpEnableHistoricalVisualBackfill = true
InpClearPhase06ObjectsOnInit = true
```

## Automated validation

```powershell
python research/exp0017_phase06/tests/test_hotfix011_raw_path_freshness.py -v
python tools/engineering/validate_alpha_lab_policy.py
python tools/engineering/check_mql5_compatibility.py
python tools/engineering/audit_repository_layout.py
python docs/ai_algorithm_engineering_os/tools/validate_vault.py
```
