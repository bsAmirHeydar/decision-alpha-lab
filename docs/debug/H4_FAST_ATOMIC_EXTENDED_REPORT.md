# H4 Fast Atomic Extended Report

This update keeps the official H4 report no-sample and fast, while restoring useful diagnostics that were previously only visible in the legacy sample report.

The report still uses `sampleCalls=0`, `branchSamplesBuilt=0`, `m0002Calls=0`, and `m0001ComputePasses=1`. It does not run strict prefix replay by default.

New lightweight outputs:

- `DAL_D0010_ATOMIC_LAG_DECAY`
- `DAL_D0010_ATOMIC_RUN_LENGTH_TRANSITION`
- `DAL_D0010_ATOMIC_BLOCK_PROFILE_FAST`
- `DAL_D0010_ATOMIC_BLOCK_PROFILE_MAIN`
- `DAL_D0010_ATOMIC_BLOCK_PROFILE_SLOW`

These diagnostics are computed over pure known-time batches, so events that become known on the same candle are never treated as sequential. Mixed reversal/continuation batches remain ambiguous and are skipped from transition/run statistics by default.
