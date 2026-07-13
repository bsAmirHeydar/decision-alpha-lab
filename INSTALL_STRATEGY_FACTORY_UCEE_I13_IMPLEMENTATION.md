# Install UCE-I13 Patch

Extract the patch into the repository root. Validate the file index, run phase tests, cumulative UCEE tests, boundary checks, MQL5 static checks, delivery validation, and engineering policy. Stage only paths listed by `UCEE_I13_FILE_INDEX.txt`.

The patch does not claim MetaEditor compilation. Run `tools/strategy_factory/compile_uce_i13_hybrid_policy.ps1` on the target Windows/MetaTrader installation and retain the real compiler logs.
