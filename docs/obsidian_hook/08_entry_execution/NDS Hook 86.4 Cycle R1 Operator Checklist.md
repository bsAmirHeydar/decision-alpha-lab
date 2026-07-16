# NDS Hook 86.4 Cycle R1 Operator Checklist

## Before test

- [ ] Patch hashes verified.
- [ ] Python unit tests and both static Hook trade QAs pass.
- [ ] Central and lightweight EAs compile in supported MetaEditor.
- [ ] Expert is `NDSHookLimitF123Backtest`.
- [ ] Actual tester input `InpBTTradeProfile=HOOK_864_CYCLE_R1`.
- [ ] `InpBTProfile=PARITY` and `InpBTPrintRunSummary=true` for diagnosis.
- [ ] Ratio 0.864, closure 0.50, X 3/4, confirmed Terminal, Phase04 X closed, untouched after closure, R 1.0.
- [ ] Dedicated magic/account/symbol selected.
- [ ] Risk/volume and Stop buffer reviewed.

## Paper mode

- [ ] `Enabled=true`.
- [ ] `SendLiveOrders=false`.
- [ ] Funnel confirms Phase02→Phase03→Phase04→untouched→ready progression.
- [ ] Ledger confirms closure/first-arrival evidence and stable setup key.

## Demo broker mode

- [ ] Explicit approval exists.
- [ ] Limit, SL, and TP supported.
- [ ] Stops/freeze levels captured.
- [ ] One pending/position maximum verified.
- [ ] x3→x4 does not reprice or duplicate.
- [ ] Hook death cancellation tested.
- [ ] Restart recovers pending/position profile without switching exit doctrine.
- [ ] Broker-held pending and position SL/TP geometry remains at least 1R.
- [ ] Invalid fixed-R pending protection is cancelled; failed cancellation creates a blocking incident.
- [ ] Recovered exposure rows are written to the Phase 55 ledger even when current input profile differs.

## Incident

- [ ] Disable send authority.
- [ ] Preserve Journal/Experts/ledger/broker state.
- [ ] Do not reset used setups before reconciliation.


## Zero-trade review

- [ ] Read `dominant_blocker`; do not loosen doctrine blindly.
- [ ] Confirm `p02_sequences`, `p03_records`, `p04_closed`, `p04_evidence_total`, `untouched864_total`, and `ready_runs`.
- [ ] If ready exists, inspect paper/send authority, one-attempt registry, existing exposure, price-side, stops/freeze, volume, margin and session gates.
- [ ] Preserve Strategy Tester Journal and parameter set as evidence.
