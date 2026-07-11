# Compile and Test Runbook

## 1. Python and static checks

From repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\run_phase01_tests.ps1
```

Expected:

- Python compileall succeeds.
- Phase 01 pytest suite passes.
- MQL5 compatibility scanner reports zero errors.
- Registry validation returns PASS.

## 2. MetaEditor compilation

Provide the actual MetaEditor executable and terminal MQL5 data root:

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\tools\strategy_factory\compile_sf01_contracts.ps1 `
  -MetaEditorPath "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  -TerminalMql5Root "C:\Users\<USER>\AppData\Roaming\MetaQuotes\Terminal\<INSTANCE>\MQL5"
```

The script stages headers and the self-test EA into the selected terminal tree, compiles, prints the log, and fails on compiler errors.

## 3. Strategy Tester self-test

Run `SF01_ContractSelfTest` on any symbol/timeframe. It does not trade. `OnInit` must return success and the Experts log must show all assertions as PASS with zero failures.

## 4. Attach evidence

Store the MetaEditor log and tester log under a local evidence directory or commit a sanitized QA record. Phase 02 must not change a contract to fix packaging without rerunning these tests.

## Troubleshooting

- Include not found: verify staging path under `MQL5/Include/AlphaLab/StrategyFactory/Contracts`.
- Golden ID mismatch: check canonical field ordering, enum names, and UTF-16LE hashing.
- Timestamp rejection: verify UTC milliseconds and source offset.
- Test import failure: run from repository root and set `PYTHONPATH` through the provided script.
