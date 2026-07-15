# NDS Hook 86.4 Cycle R1 Operator Checklist

## Before test

- [ ] Patch hashes verified.
- [ ] Python unit tests and both static Hook trade QAs pass.
- [ ] Central and lightweight EAs compile in supported MetaEditor.
- [ ] `HOOK_864_CYCLE_R1` selected deliberately.
- [ ] Ratio 0.864, X 3/4, confirmed Terminal true, untouched true, R 1.0.
- [ ] Dedicated magic/account/symbol selected.
- [ ] Risk/volume and Stop buffer reviewed.

## Paper mode

- [ ] `Enabled=true`.
- [ ] `SendLiveOrders=false`.
- [ ] Ledger confirms first-arrival and stable setup key.

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
