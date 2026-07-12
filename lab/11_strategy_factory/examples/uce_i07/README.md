# UCE-I07 examples

These examples prove exact trainer routing, OOF prediction, final-test sealing, deterministic reruns, serialization parity, and model-artifact packaging. The reference trainers are intentionally weak conformance baselines.

```powershell
$env:PYTHONPATH=(Resolve-Path ".\lab\11_strategy_factory\python").Path
python -m strategy_factory_trainers_v3.cli conformance
python -m strategy_factory_trainers_v3.cli registry
```
