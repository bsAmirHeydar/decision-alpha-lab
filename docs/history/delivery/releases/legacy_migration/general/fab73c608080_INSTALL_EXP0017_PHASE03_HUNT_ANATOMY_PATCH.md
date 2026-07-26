# Install EXP0017 Phase 03 Hunt Anatomy Patch

This patch adds the Phase 03 Hunt Anatomy layer for EXP0017.

## Install

Run from the repository root:

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-phase03-hunt-anatomy-code-docs-obsidian-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-phase03-hunt-anatomy-code-docs-obsidian-patch.zip"
```

## Expert added

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Hunt_Anatomy.mq5
```

## Safety

This phase does not trade. It only detects raw high/low hunts against Phase 02 references.
