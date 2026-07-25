# Install and Validate UCEE-I03

1. Extract the patch at repository root.
2. Run `python tools/engineering/run_engineering_policy.py .`.
3. Run `python tools/strategy_factory/check_uce_i03_boundaries.py .`.
4. Run `python tools/strategy_factory/check_uce_i03_mql5_static.py .`.
5. Run `python tools/strategy_factory/validate_uce_i03_delivery.py .`.
6. Set `PYTHONPATH` to `lab/11_strategy_factory/python`.
7. Run the I01, I02, and I03 pytest suites.
8. Compile the MQL5 diagnostic and self-test with MetaEditor on Windows.
9. Run the self-test EA in a non-trading chart. It has no broker authority.
