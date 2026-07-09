# Install Gartal Terminal Architecture Start Patch

Run from repository root in PowerShell:

```powershell
Expand-Archive -Path .\gartal_terminal_architecture_start_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_architecture_start_patch.zip -Force
```

Then inspect:

```powershell
git status
```

Recommended commit:

```powershell
git add product_lab/indicators/gartal_terminal/obsidian docs/patches/gartal_terminal_architecture_start
git commit -m "docs(gartal-terminal): add detailed architecture start" -m "Add English Obsidian-native architecture start for gartal terminal. Define system architecture, MQL5 module contracts, data pipeline, Forex Factory parser contract, broker GMT normalization, runtime dashboard filters, alert state machine, chart rendering object model, cache resilience, engineering execution order, ADRs, and Obsidian canvas for the implementation path."
```
