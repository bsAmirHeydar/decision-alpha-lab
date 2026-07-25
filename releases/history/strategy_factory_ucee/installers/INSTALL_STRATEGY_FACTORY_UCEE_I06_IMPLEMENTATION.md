# Install UCEE-I06

1. Extract the patch at repository root.
2. Run `python tools/engineering/run_engineering_policy.py .`.
3. Run `python tools/strategy_factory/check_uce_i06_boundaries.py .`.
4. Run `python tools/strategy_factory/check_uce_i06_mql5_static.py .`.
5. Set `PYTHONPATH` to `lab/11_strategy_factory/python` and run `python -m strategy_factory_dataset_v3.cli conformance`.
6. Run cumulative pytest through `tools/strategy_factory/run_uce_i06_tests.ps1`.
7. Compile the three MQL5 targets locally with MetaEditor using `compile_uce_i06_dataset.ps1`.
