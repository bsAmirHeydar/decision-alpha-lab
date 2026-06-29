# Apply Flag Optionality / X-Y State Philosophy Patch

Run these commands from the root of `decision-alpha-lab` in Windows PowerShell:

```powershell
Expand-Archive -Path .\flag_optionality_xy_state_philosophy_patch.zip -DestinationPath .\_patch_flag_optionality_xy -Force
Remove-Item .\flag_optionality_xy_state_philosophy_patch.zip -Force
git apply .\_patch_flag_optionality_xy\flag_optionality_xy_state_philosophy.patch
```

Then review:

```powershell
git status
git diff --stat
```

Commit:

```powershell
git add .

git commit -m @"
Add Flag optionality and X/Y state philosophy README

- Add a second English philosophy README for the Flag Project
- Document the practical trading experience behind optionality-based reward design
- Formalize the distinction between X-axis structural liquidity location and Y-axis live energy state
- Explain why one-state market thinking breaks during transitions between reversals, sweeps, rallies, and continuation
- Reframe hooks as structural context rather than automatic entry rules
- Define F-counting as Y-axis energy analysis instead of mechanical pattern counting
- Document the scale problem and the principle that scale must be earned by structure, not selected arbitrarily by timeframe
- Separate liquidity grabs from real rallies as a central research axis
- Add optionality as a payoff-permission layer based on limited risk, clean path, structural room, and fat-tail expansion potential
- Translate the philosophy into X-map, Y-state, scenario engine, and optionality filter modules
- Add research questions, validation metrics, and development priorities for future Flag experiments
"@
```
