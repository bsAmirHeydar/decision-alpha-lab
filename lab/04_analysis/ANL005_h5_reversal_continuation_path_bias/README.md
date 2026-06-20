# ANL005 — H5 Reversal/Continuation Path Bias Review

## Question

Which H5 results are tradable, and which are only structural path statistics?

---

## Key finding

The classic H5 report mixed structural path normalization with execution-like R metrics.

Reversal fixed-R tests were closer to execution logic. Continuation path PF was not a real trading PF because continuation did not use a real initial stop in the classic report.

---

## Reversal interpretation

Reversal showed short reaction behavior but weak full structural path performance.

Practical implication:

- use touch-entry,
- test R1/R2,
- account for same-bar ambiguity and spread.

---

## Continuation interpretation

Continuation showed large path potential. However, old PF must be retested with explicit risk.

Practical implication:

- use ATR or structural stop,
- test close-break and intrabar-break separately,
- test trailing and fixed R separately,
- distinguish path R from execution R.

---

## Research decision

H5 main reports must default to atomic no-sample replay with explicit risk mode.
