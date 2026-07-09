# Install — Stage 06 Runtime Filter Engine

Run from repository root:

```powershell
Expand-Archive -Path .\gartal_terminal_stage06_runtime_filters_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_stage06_runtime_filters_patch.zip -Force
```

Then validate:

```powershell
.\product_lab\indicators\gartal_terminal\scripts\Check-GartalStage06.ps1
```

Compile manually in MetaEditor:

```text
product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5
```
