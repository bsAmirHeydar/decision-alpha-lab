# Install Phase 20

1. Extract at repository root.
2. Run `python tools/engineering/run_engineering_policy.py .`.
3. Run `python tools/strategy_factory/check_sf20_boundaries.py .`.
4. Run `python tools/strategy_factory/check_sf20_mql5_static.py .`.
5. Run `pytest -q lab/11_strategy_factory/tests/phase20_integration`.
6. Compile locally with `tools/strategy_factory/compile_sf20_integration.ps1`.
7. Run `SF20_EXP0017IntegrationSelfTest` and `SF20_EXP0017Diagnostic`.
8. Run audit-only differential replay before pilot shadow mode.
