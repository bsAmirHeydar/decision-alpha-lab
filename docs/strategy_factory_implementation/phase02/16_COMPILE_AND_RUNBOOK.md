# Compile and Runbook

## Python and Static Tests

```powershell
powershell -ExecutionPolicy Bypass -File .	ools\strategy_factoryun_phase02_tests.ps1
```

## MetaEditor Compile

```powershell
powershell -ExecutionPolicy Bypass `
  -File .	ools\strategy_factory\compile_sf02_runtime.ps1 `
  -MetaEditorPath "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  -TerminalMql5Root "C:\Users\<USER>\AppData\Roaming\MetaQuotes\Terminal\<INSTANCE>\MQL5"
```

Compile both the Host and Self-Test EA. Run the Self-Test on any chart and confirm `failed=0`.
