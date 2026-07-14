feat(exp0019): implement FP-I15 paper execution and risk geometry

- add protected-symbol setup-to-plan adapter
- add exact SELL stop plus one spread and worst-case risk sizing
- add explicit paper quota policy matrix and atomic reservation
- add synthetic order, fill, position, reconciliation, and restart layers
- add paper-only MQL5 EA and self-test
- keep FP-DEC-012 unset and live broker authority disabled
