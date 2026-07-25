# Install — EXP0017 Phase 02 Reference Field Anatomy Patch

This patch adds Phase 02 Reference Field Anatomy.

It assumes Phase 01 Time Anatomy has already been installed because Phase 02 imports `CGT_Types.mqh` and `CGT_Time.mqh`.

## Install

From repository root:

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-phase02-reference-field-code-docs-obsidian-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-phase02-reference-field-code-docs-obsidian-patch.zip"
```

Then compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Reference_Anatomy.mq5
```

## Safety

This expert does not trade. It does not detect hunts or divergences. It only builds and displays same-day CG reference high/low values for two symbols.
