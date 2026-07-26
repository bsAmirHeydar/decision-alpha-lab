# Installation and Verification — UCEE-I04

1. Expand the patch at repository root.
2. Run `tools/strategy_factory/run_uce_i04_tests.ps1`.
3. On Windows with MetaTrader 5 installed, run `tools/strategy_factory/compile_uce_i04_treatment_compiler.ps1` with the correct MetaEditor path.
4. Execute `UCE_I04_TreatmentCompilerSelfTest.mq5` and confirm a PASS journal entry.
5. Commit only after engineering policy, vector verification, cumulative Python tests, and local MetaEditor compilation pass.

The patch is additive. It requires UCE-I01, UCE-I02, and UCE-I03 to already be present.
