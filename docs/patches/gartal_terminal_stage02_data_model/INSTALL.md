# Install

From the repository root in PowerShell:

```powershell
Expand-Archive -Path .\gartal_terminal_stage02_data_model_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_stage02_data_model_patch.zip -Force
```

Then run:

```powershell
.\product_lab\indicators\gartal_terminal\scripts\Check-GartalStage02.ps1
```

Compile `product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5` in MetaEditor.
