# Install EXP0017 Phase 06 Hotfix004 — Real Drawing Lines

This patch repairs Phase 06 when the chart shows text labels but the actual divergence lines, markers, and verticals are not visible.

Install from repository root:

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-phase06-hotfix004-real-drawing-lines-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-phase06-hotfix004-real-drawing-lines-patch.zip"
```

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

Important input:

```text
InpForceAllVisualObjectsOn = true
```
