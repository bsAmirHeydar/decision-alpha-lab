# Install FP-I13

1. Extract the ZIP into the repository root.
2. Verify `EXP0019_FP_I13_FILE_HASHES.sha256`.
3. Run the FP-I13 Python tests and validators.
4. Sync `mql5` into the MetaTrader terminal data folder.
5. Run `tools/exp0019/run_fp_i13_local_acceptance.ps1`.
6. Attach `EXP0019_FP_I13_ReleaseSelfTest` and verify PASS.
7. Attach the production indicator on two charts with different display timeframes.
8. Record local performance and collision evidence using the templates under `phase_deliveries/fp_i13/templates`.
