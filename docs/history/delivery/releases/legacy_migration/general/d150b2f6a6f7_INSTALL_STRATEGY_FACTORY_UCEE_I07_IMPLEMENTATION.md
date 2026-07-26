# Install and Verify UCEE-I07

1. Extract the ZIP at repository root.
2. Run `python tools/engineering/run_engineering_policy.py .`.
3. Run the I07 boundary, MQL5 static, and delivery validators.
4. Set `PYTHONPATH` to `lab/11_strategy_factory/python`.
5. Run `python -m strategy_factory_trainers_v3.cli conformance`.
6. Verify golden vectors with `python tools/strategy_factory/generate_uce_i07_vectors.py . --verify-only`.
7. Run cumulative I01–I07 pytest through `tools/strategy_factory/run_uce_i07_tests.ps1`.
8. On Windows with MT5 installed, compile the three MQL5 targets using `compile_uce_i07_trainers.ps1` and retain clean MetaEditor logs as local acceptance evidence.

Do not treat the three reference trainers as production trading models. UCE-I08 introduces the classical tabular algorithm pack through the same SDK.
