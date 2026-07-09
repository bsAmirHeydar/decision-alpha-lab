# Install

Place the zip in the project root and run:

```powershell
Expand-Archive -Path .\gartal_terminal_stage10_product_hardening_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_stage10_product_hardening_patch.zip -Force
```

Then run:

```powershell
.\product_lab\indicators\gartal_terminal\scripts\Check-GartalStage10.ps1
```

Compile both MQL5 files in MetaEditor:

```text
product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5
product_lab/indicators/gartal_terminal/mql5/experts/GartalNewsDownloaderEA.mq5
```
