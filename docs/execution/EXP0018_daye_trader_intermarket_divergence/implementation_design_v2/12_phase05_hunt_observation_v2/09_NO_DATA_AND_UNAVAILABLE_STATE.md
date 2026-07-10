---
id: EXP0018-P05-NO-DATA
title: "P05 No Data and Unavailable State"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# No Data

Missing symbol history, incomplete reference periods, invalid OHLC, or absent P04 context produce `UNAVAILABLE`. They never produce `NOT_HUNTED`.

This distinction prevents a missing second symbol from being misclassified as Protected and generating a false one-sided hunt.
