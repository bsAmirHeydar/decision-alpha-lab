# NDS Hook 86.4 Cycle R1 — Exact Speed v1.2.0

This bounded patch accelerates the dedicated MT5 Strategy Tester without changing the PARITY data universe or trading result contract.

## Implemented

- broker-state fast path before `CopyRates` for pending orders and fixed-1R positions;
- preservation of the full F graph for legacy `TERMINAL_F123` positions;
- demand-driven F1/F2/F3 construction for new 86.4 candidates;
- candidate-scoped canonical Phase03/04 processing;
- binary first-arrival start at closure time;
- sequence-id lookup hint with structural identity verification and fallback;
- single-pass diagnostic funnel and latest-candidate selection;
- parallel, deterministic, non-fail-fast bounded QA runner;
- runtime telemetry for every acceleration decision;
- full reference mode through `InpBTExactAcceleration=false`.

## Accuracy preserved

PARITY remains 5000 closed bars and all eight scales: `2,3,5,8,13,21,34,55`. No threshold, Hook definition, node count, closure rule, first-touch rule, broker normalization, risk sizing, order lifecycle or tick model is relaxed.

## External boundary

MetaEditor compilation and MT5 paired performance/parity runs remain external Windows evidence. The repository environment does not contain MetaEditor or the MT5 Strategy Tester.
