# INSTALL — EXP0017 Chapter 16 Decision Model Patch

This patch adds Chapter 16 strategy-architect documentation and Obsidian knowledge notes for the Cycle Group Intermarket Divergence project.

## Scope

Chapter 16 defines the statistical model / AI decision-support layer.

The model:

- studies only confirmed historical signals at the base stage;
- analyzes all cycle groups together and separately;
- scores quality through statistical components;
- does not enter trades;
- does not exit trades;
- does not override execution;
- does not become an autonomous trading authority;
- supports the strategy architect in choosing which rules, filters, weights, or changes may later be activated.

## Install

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-chapter16-decision-model-expanded-obsidian-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-chapter16-decision-model-expanded-obsidian-patch.zip"
```
