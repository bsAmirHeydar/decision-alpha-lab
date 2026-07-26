# LEVEL 21 — STC SMT Drawing Audit Hardening

Level 21 is a visual verification patch for `EXEC001_STC_SMT_Cycles`.

It improves the chart overlay so an operator can verify the locked STC rules directly on the active `Symbol1` or `Symbol2` chart:

- New York STC session structure.
- M cycles and no-entry gaps.
- W boundaries and closed W high/low levels.
- Recent check-candle boxes.
- W1 no-signal and final-check no-entry conditions.
- Raw previous-W hunt markers.
- BOTH-hunted no-SMT cases.
- Clean-symbol SMT side and selected reference.
- Paper entry, SL, TP, W4 partial marker, 15:30 hard-close marker and outcome labels.

No trading logic changes were made.

The patch also fixes the hard-close compile warning by explicitly casting `SYMBOL_SPREAD` to `double` before reporting cost calculations.
