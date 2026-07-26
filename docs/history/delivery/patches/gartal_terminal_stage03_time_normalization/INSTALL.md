# Install

From the repository root in PowerShell:

```powershell
Expand-Archive -Path .\gartal_terminal_stage03_time_normalization_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_stage03_time_normalization_patch.zip -Force
```

Then run:

```powershell
.\product_lab\indicators\gartal_terminal\scripts\Check-GartalStage03.ps1
```
