# Install — Stage 09 Resilience Patch

Place the zip in the repository root and run:

```powershell
Expand-Archive -Path .\gartal_terminal_stage09_resilience_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_stage09_resilience_patch.zip -Force
```

Then run:

```powershell
.\product_lab\indicators\gartal_terminal\scripts\Check-GartalStage09.ps1
```

Compile in MetaEditor:

```text
product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5
product_lab/indicators/gartal_terminal/mql5/experts/GartalNewsDownloaderEA.mq5
```
