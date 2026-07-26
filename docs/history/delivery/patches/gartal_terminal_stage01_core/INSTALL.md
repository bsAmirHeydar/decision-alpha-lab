# Install — gartal terminal Stage 01 Core Skeleton

Place the zip in the repository root, then run:

```powershell
Expand-Archive -Path .\gartal_terminal_stage01_core_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_stage01_core_patch.zip -Force
```

## Compile path

Open this file in MetaEditor:

```text
product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5
```

If your MetaEditor cannot compile from the repo folder, copy this folder structure into your terminal data directory:

```text
MQL5/Indicators/GartalTerminal/GartalTerminal.mq5
MQL5/Indicators/GartalTerminal/include/*.mqh
```

## Default runtime

The indicator defaults to sample data:

```text
InpUseSampleData = true
```

Forex Factory direct parsing is intentionally not active in this stage.
