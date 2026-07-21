# Install NDS Hook 86.4 Compile Hotfix v1.1.1

## Dependency

The v1.1.0 no-trade engine fix must already be installed.

## Install and verify

```powershell
Expand-Archive ".\decision-alpha-lab-nds-hook-864-cycle-r1-compile-hotfix-v1.1.1.zip" -DestinationPath "." -Force
Remove-Item ".\decision-alpha-lab-nds-hook-864-cycle-r1-compile-hotfix-v1.1.1.zip" -Force
powershell -ExecutionPolicy Bypass -File .\tools\flag_counting\run_nds_hook_864_cycle_r1_tests.ps1
```

## Compile

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\flag_counting\compile_nds_hook_864_cycle_r1.ps1 -MetaEditorPath "C:\Path\To\metaeditor64.exe"
```
