# Install EXP0018 Implementation Design v2 Patch

## Purpose

Install the detailed P00–P20 implementation-design program, Obsidian maps, contracts, registries and validation tooling. No strategy MQL5 behavior is changed.

## Install

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0018-implementation-design-v2-docs-obsidian-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0018-implementation-design-v2-docs-obsidian-patch.zip"

.\lab\10_infrastructure\EXP0018_daye_trader\powershell\run_exp0018_implementation_design_v2_checks.ps1 -RepoRoot "."
```

## Start

Open:

`docs/execution/EXP0018_daye_trader_intermarket_divergence/implementation_design_v2/EXP0018_IMPLEMENTATION_DESIGN_V2_INDEX.md`
