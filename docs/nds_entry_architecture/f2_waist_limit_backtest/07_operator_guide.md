# F2 Waist Limit — Operator Guide

## Tester executable

Select:

```text
NDSF2WaistLimitBacktest
```

## First fast run

```text
InpF2BTProfile = FAST
InpF2BTTradeEnabled = true
InpF2BTSendTesterOrders = true
InpF2BTEntryOffsetPoints = 1
InpF2BTMaxSetupAgeBars = 1
InpF2BTOneAttemptPerF2 = true
InpF2BTResetUsedSetupsOnInit = true
```

After the first initialization, set `InpF2BTResetUsedSetupsOnInit=false` when testing restart persistence rather than a clean run.

## Journal startup contract

```text
NDS_F2_BT_INIT status=ready
contract=F2_confirmed_to_waist_limit_F1_waist_SL_F2_leg2_TP
hooks_as_entry=false zones=false ai=false
```

## Final verification

Run the same test with `PARITY`. FAST is intended for development speed, not final equivalence claims.
