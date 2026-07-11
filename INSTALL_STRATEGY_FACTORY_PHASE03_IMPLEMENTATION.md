# Install Phase 03

Prerequisites:

1. Phase 01 contracts installed.
2. Phase 02 runtime foundation installed.
3. Repository working tree reviewed or clean.

From the repository root:

```powershell
Expand-Archive `
  -Path ".\decision-alpha-lab-strategy-factory-phase03-shared-market-services.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  ".\decision-alpha-lab-strategy-factory-phase03-shared-market-services.zip" `
  -ErrorAction SilentlyContinue
```

Run automated tests:

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\tools\strategy_factory\run_phase03_tests.ps1
```

Compile MQL5 locally:

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\tools\strategy_factory\compile_sf03_market_services.ps1 `
  -MetaEditorPath "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  -TerminalMql5Root "C:\Users\<USER>\AppData\Roaming\MetaQuotes\Terminal\<INSTANCE>\MQL5"
```
