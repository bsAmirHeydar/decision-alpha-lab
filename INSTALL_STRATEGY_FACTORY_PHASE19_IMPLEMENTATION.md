# Install Strategy Factory Phase 19

1. Extract the patch at the repository root.
2. Run `python tools/engineering/run_engineering_policy.py .`.
3. Run `python tools/strategy_factory/check_sf19_boundaries.py .`.
4. Run `python tools/strategy_factory/check_sf19_mql5_static.py .`.
5. Run `pytest -q lab/11_strategy_factory/tests/phase19_monitoring`.
6. Run `tools/strategy_factory/compile_sf19_monitoring.ps1` on Windows with MetaTrader 5 installed.
7. Attach `SF19_ObservabilityDiagnostic` and `SF19_ObservabilitySelfTest` to a controlled demo/test environment.
8. Preserve compile logs, telemetry replay evidence, health reports, and alert transition evidence.
9. Do not integrate a real anatomy or enable live authority until the Phase 19 handoff preconditions are met.

## Rollback

Remove only Phase 19-owned files and restore the previous `pyproject.toml`. Phase 18 live authority and its kill switch remain unchanged. Historical monitoring evidence should remain append-only and must not be rewritten.
