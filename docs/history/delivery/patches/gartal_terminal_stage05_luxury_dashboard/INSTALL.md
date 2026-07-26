# Install — Gartal Terminal Stage 05

Run from repository root in PowerShell:

```powershell
Expand-Archive -Path .\gartal_terminal_stage05_luxury_dashboard_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_stage05_luxury_dashboard_patch.zip -Force
```

Then:

```powershell
.\product_lab\indicators\gartal_terminal\scripts\Check-GartalStage05.ps1
```

Compile `product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5` in MetaEditor.
