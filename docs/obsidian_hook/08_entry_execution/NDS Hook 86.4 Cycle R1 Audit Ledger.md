# NDS Hook 86.4 Cycle R1 Audit Ledger

## File

```text
MQL5/Files/FlagCountingPhoenix/nds_hook_864_cycle_r1_trade_ledger.csv
```

## Evidence

The row includes profile/schema, canonical sequence/family/direction, X count, Origin/Crown/Terminal, Terminal retracement, entry ratio, untouched decision, Entry/Death/Stop/Target, risk/reward/R, volume, setup key, exposure counts, tickets, action, status, and reason.

## Separation

The Phase 52 terminal/F123 ledger is retained separately. Analysts must not combine both schemas without an explicit profile dimension. On restart, routing follows the profile recovered from the Magic-owned broker exposure rather than mutable current inputs. Recovered rows preserve actual broker Entry/SL/TP and realized protection geometry.

## Review questions

1. Was the level untouched at decision time?
2. Did X count equal 3 or 4?
3. Does Entry recompute to Crown→Origin 0.864 within tick normalization?
4. Is Stop behind Death/Origin?
5. Is normalized reward at least one R?
6. Did one Hook produce only one setup key?
