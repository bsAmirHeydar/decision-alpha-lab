# INSTALL — EXP0017 Chapter 13 Statistical Uncertainty Patch

This patch adds the Chapter 13 strategy-architect doctrine for EXP0017 Cycle Group Intermarket Divergence.

## Theme

Chapter 13 formalizes a strict epistemic boundary:

> We do not know whether a proposed difference, preference, filter, quality distinction, timing distinction, symbol distinction, cycle-group distinction, or reference distinction matters until it is tested statistically.

The chapter prevents premature narrative fitting. It preserves every raw divergence for later classification while keeping future ideas in a separate research backlog.

## Install

From the repository root:

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-chapter13-statistical-uncertainty-expanded-obsidian-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-chapter13-statistical-uncertainty-expanded-obsidian-patch.zip"
```

## Scope

Added:

- strategy-architect Chapter 13 documents
- deep Obsidian concept notes
- decision maps
- review checklist
- document cards
- MOC update

Not added:

- no code
- no EA implementation
- no MQL5 changes
- no statistical engine changes
- no filter logic
- no execution change
