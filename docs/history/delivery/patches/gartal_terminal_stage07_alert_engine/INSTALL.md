# Install — Stage 07 Alert Engine

Place the zip in the repository root and run:

```powershell
Expand-Archive -Path .\gartal_terminal_stage07_alert_engine_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_stage07_alert_engine_patch.zip -Force
```

Then validate:

```powershell
.\product_lab\indicators\gartal_terminal\scripts\Check-GartalStage07.ps1
```

Compile in MetaEditor:

```text
product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5
```
