# Install Phase 17

1. Extract the patch at the repository root.
2. Run `python .\tools\engineering\run_engineering_policy.py .`.
3. Run `.\tools\strategy_factory\run_phase17_tests.ps1`.
4. Compile Phase 17 EAs with `.\tools\strategy_factory\compile_sf17_execution.ps1`.
5. Run `SF17_PaperExecutionSelfTest` in MetaTrader 5 and retain the terminal log.
6. Use `SF17_PaperShadowHost` only in paper or shadow mode. It has no live order authority.
