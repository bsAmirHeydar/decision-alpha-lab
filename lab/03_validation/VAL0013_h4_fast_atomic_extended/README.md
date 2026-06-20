# VAL0013 — H4 Fast Atomic Extended Diagnostics

Purpose: restore rich H4 reporting without returning to the old sample-based report or the heavy strict prefix replay.

Contract:

- No M0002 branch samples.
- No outcome-sorted sample sequence.
- Raw M0001 events are grouped by known candle/time.
- Same-known-time events are simultaneous.
- Mixed reversal/continuation batches are ambiguous and skipped.
- M0001 is computed once in the main fast mode.

Use `InpAtomicPrintExtendedReport=true` to print lightweight lag decay, run-length transition, and block profile diagnostics.
