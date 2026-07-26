# Install

Run from repository root:

```powershell
Expand-Archive -Path .\gartal_terminal_stage08_source_adapter_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_stage08_source_adapter_patch.zip -Force
```

Then check:

```powershell
.\product_lab\indicators\gartal_terminal\scripts\Check-GartalStage08.ps1
```

Compile in MetaEditor:

```text
product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5
product_lab/indicators/gartal_terminal/mql5/experts/GartalNewsDownloaderEA.mq5
```
