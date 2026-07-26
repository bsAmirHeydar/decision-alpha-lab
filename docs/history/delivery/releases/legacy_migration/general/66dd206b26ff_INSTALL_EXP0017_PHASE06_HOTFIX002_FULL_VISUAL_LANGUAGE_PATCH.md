# INSTALL — EXP0017 Phase 06 Hotfix002 Full Visual Language

This patch upgrades Phase 06 drawing from a simple reference-to-confirmation audit line into a complete divergence visual language.

## Install

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-phase06-hotfix002-full-visual-language-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-phase06-hotfix002-full-visual-language-patch.zip"
```

## Compile target

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

## Prerequisite

Phase 06 and Hotfix001 confirmation-dependency patch must be installed first, because this patch still consumes Phase 05 confirmation states.
