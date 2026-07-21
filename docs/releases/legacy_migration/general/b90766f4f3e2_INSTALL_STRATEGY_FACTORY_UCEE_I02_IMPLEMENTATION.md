# Install UCEE-I02

1. Extract the patch at the repository root with overwrite enabled.
2. Run the engineering policy, boundary, MQL5 static, delivery, compileall, and pytest gates.
3. Run both reference-package conformance commands.
4. Compile the three UCE-I02 MQL5 targets with MetaEditor on Windows.
5. Execute the MQL5 self-tests in MetaTrader or Strategy Tester.
6. Commit only the explicit UCE-I02 paths.

## Local Test Command

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\run_uce_i02_tests.ps1
```

## MetaEditor Compile Command

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\compile_uce_i02_contexts.ps1
```

MetaEditor compilation is an external acceptance gate. Static Linux checks do not replace it.
