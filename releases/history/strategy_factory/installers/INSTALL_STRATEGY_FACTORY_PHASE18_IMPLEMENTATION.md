# Install Phase 18

1. Extract the patch into the repository root.
2. Run `python tools/engineering/run_engineering_policy.py .`.
3. Run `python tools/strategy_factory/check_sf18_boundaries.py .`.
4. Run `python tools/strategy_factory/check_sf18_mql5_static.py .`.
5. Run `pytest -q lab/11_strategy_factory/tests/phase18_live`.
6. Compile all Phase 18 EAs locally with MetaEditor and retain the compiler log.
7. Run the self-test and diagnostic on a demo terminal.
8. Keep `InpEnableMicroLive=false` and `InpStartWithKillSwitchEngaged=true` until the complete demo rehearsal, ledger validation, reconciliation and operator drill are signed off.

No repository artifact contains an operator secret. Only hashes are committed.
