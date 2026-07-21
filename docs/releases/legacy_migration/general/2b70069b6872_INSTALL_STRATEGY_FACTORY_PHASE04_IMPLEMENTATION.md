# Install Strategy Factory Phase 04

Prerequisites: Phase 01, Phase 02 and Phase 03 are already installed.

```powershell
Expand-Archive `
  -Path ".\decision-alpha-lab-strategy-factory-phase04-static-plugin-registry.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  ".\decision-alpha-lab-strategy-factory-phase04-static-plugin-registry.zip" `
  -ErrorAction SilentlyContinue
```

Run tests:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\run_phase04_tests.ps1
```

Compile locally with MetaEditor:

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\tools\strategy_factory\compile_sf04_plugins.ps1 `
  -MetaEditorPath "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  -TerminalMql5Root "C:\Users\<USER>\AppData\Roaming\MetaQuotes\Terminal\<INSTANCE>\MQL5"
```
