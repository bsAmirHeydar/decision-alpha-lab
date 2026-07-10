---
id: EXP0018-P05-SYMBOL-LOCAL
title: "P05 Symbol-Local Comparison Contract"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Symbol-Local Comparison

Every price is compared only within the same symbol:

- SPX current high versus SPX reference high;
- NDX current high versus NDX reference high;
- SPX current low versus SPX reference low;
- NDX current low versus NDX reference low.

Cross-symbol price subtraction is forbidden because the price scales are unrelated. The stored penetration value is symbol-local and must never be compared numerically across symbols without a separately approved normalization contract.
