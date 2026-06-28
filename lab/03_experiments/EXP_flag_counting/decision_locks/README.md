# Flag Counting Phoenix Decision Locks

Level 17 writes the decision-lock state of the current run. Use it after the
acceptance matrix to verify that the chart/run is not relying on unresolved or
implicit defaults.

Recommended MT5 preset for a decision-lock review:

```text
InpReleaseProfile = FP_RELEASE_PROFILE_CLEAN_MAIN
InpAcceptanceEnabled = true
InpAmbiguityEnabled = true
InpAmbiguityWriteCsv = true
InpAmbiguityMode = FP_AMBIGUITY_MODE_OBSERVE
```

For a stricter release review:

```text
InpAmbiguityMode = FP_AMBIGUITY_MODE_RELEASE
InpAmbiguityStrict = true
InpAmbiguityRequireNoReleaseBlockers = true
InpAcceptanceMode = FP_ACCEPTANCE_MODE_RELEASE
InpValidationEnabled = true
```

Expected output:

```text
MQL5/Files/FlagCountingPhoenix/latest_ambiguity.csv
FP_LEVEL17 ... ok=true ...
FP_SUMMARY ... ambiguity_fail=0 ... ambiguity_conflicts=0 ...
```
