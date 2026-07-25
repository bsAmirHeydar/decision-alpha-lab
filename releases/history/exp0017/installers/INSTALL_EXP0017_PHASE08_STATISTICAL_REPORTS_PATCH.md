# INSTALL — EXP0017 Phase 08 Statistical Reports Patch

This patch adds **Phase 08 — Statistical Report Engine** for EXP0017 Cycle Group Intermarket Divergence.

Phase 08 reads the Phase 07 outcome-study CSV and generates aggregated statistical reports. It does not place orders, does not filter signals, does not rank live signals, and does not mutate the strategy.

## Install

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-phase08-statistical-reports-code-docs-obsidian-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-phase08-statistical-reports-code-docs-obsidian-patch.zip"
```

## Compile

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Statistical_Report_Anatomy.mq5
```

## Output Files

By default the expert reads:

```text
EXP0017_Phase07_Outcome_Study.csv
```

and writes:

```text
EXP0017_Phase08_Overall.csv
EXP0017_Phase08_By_CG.csv
EXP0017_Phase08_By_Direction.csv
EXP0017_Phase08_By_CG_Direction.csv
EXP0017_Phase08_By_Role.csv
EXP0017_Phase08_By_CG_Direction_Role.csv
EXP0017_Phase08_Red_Flags.csv
```

## Boundary

Phase 08 is measurement-only. It does not execute or modify strategy behavior.
