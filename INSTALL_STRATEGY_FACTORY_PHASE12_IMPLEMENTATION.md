# Installation and verification

Extract at repository root, then run:

```powershell
python .\tools\engineering\run_engineering_policy.py .
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\run_phase12_tests.ps1
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\compile_sf12_validation.ps1
```

MetaEditor compilation must be executed on the local Windows terminal installation. The packaged QA report records static validation only when MetaEditor is unavailable.
