# Install and Verify UCEE-I08

1. Extract at repository root.
2. Run the Engineering Policy and I08 boundary, static, and delivery validators.
3. Set `PYTHONPATH` to `lab/11_strategy_factory/python`.
4. Install `.[ucee-classical]` for mandatory classical adapters and optionally `.[ucee-boosters]`.
5. Run `python -m strategy_factory_classical_v3.cli conformance`.
6. Verify generated vectors.
7. Run cumulative I01-I08 tests.
8. Compile the three MQL5 targets locally with MetaEditor and retain clean logs.

Do not promote a high-capacity model without a passed classical comparison report.
