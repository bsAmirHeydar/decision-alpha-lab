# VAL0012 — H4 Fast Atomic Main Report

This validation release makes the official H0004 main report fast enough for routine MetaTrader runs while preserving the no-sample known-time-batch contract.

## Contract

- No M0002 branch samples.
- Raw M0001 events only.
- Events known on the same candle/time are simultaneous.
- Mixed reversal/continuation batches are ambiguous and skipped from transition statistics.
- Main report uses one M0001 pass by default.
- Strict prefix replay remains opt-in for small audits.

## Expected audit markers

```text
DAL_D0010_START ... mode=FAST_RAW_EVENT_BATCH ... compute=M0001_once_then_known_time_batch
DAL_D0010_AUDIT ... m0001ComputePasses=1 ... prefixRebuilds=0 ... sampleCalls=0 ... m0002Calls=0
```


### Release 1.01 compile fix

`InpAtomicReportMode` is now an int input for MetaEditor safety: `0` fast official report, `1` strict prefix replay for small debug runs. Installer syncs the M0004 include to all local terminal include trees.
