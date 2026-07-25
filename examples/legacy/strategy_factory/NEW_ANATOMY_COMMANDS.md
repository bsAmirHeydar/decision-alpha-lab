# New anatomy scaffold commands

```powershell
python .\src\engine\legacy\strategy_factory\sf.py scaffold `
  EXP0019_example_anatomy `
  --output-root .\contexts\legacy\lab_experiments

python .\src\engine\legacy\strategy_factory\sf.py validate-manifest `
  .\contexts\legacy\lab_experiments\EXP0019_example_anatomy\strategy.json
```

Then complete the doctrine, adapter, strategy-specific feature list, candidate
policies, matched null, and golden fixtures. Shared statistics, validation,
training, paper, risk, and execution contracts remain unchanged.
