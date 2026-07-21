# Install — EXP0017 Phase 09 Ranking Dashboard Patch

This patch adds Phase 09 Statistical Ranking & Dashboard Anatomy.

## Install

Expand the ZIP at repository root.

## Compile

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Ranking_Dashboard_Anatomy.mq5
```

## Runtime Requirement

Run Phase 07 and Phase 08 first so Phase 09 can read:

```text
EXP0017_Phase08_Overall.csv
EXP0017_Phase08_By_CG.csv
EXP0017_Phase08_By_Direction.csv
EXP0017_Phase08_By_CG_Direction.csv
EXP0017_Phase08_By_Role.csv
EXP0017_Phase08_By_CG_Direction_Role.csv
```

## Outputs

```text
EXP0017_Phase09_Rankings_All.csv
EXP0017_Phase09_Rankings_Top.csv
EXP0017_Phase09_Rankings_Bottom.csv
EXP0017_Phase09_Shortlist.csv
EXP0017_Phase09_Dashboard.html
EXP0017_Phase09_Diagnostics.csv
```

No trading behavior is added.
