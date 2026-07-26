# 10 — Audit Ledger and Evidence Schema

## Dedicated file

```text
MQL5/Files/FlagCountingPhoenix/nds_hook_864_cycle_r1_trade_ledger.csv
```

The Phase 52 ledger remains unchanged and separate.

## Required columns

The Phase 55 row preserves:

- generation time, code version, schema version, symbol, timeframe;
- attempt/ok/action/status/reason;
- pending/position/foreign exposure counts and tickets;
- profile, sequence ID, family, direction;
- canonical X count, Origin, Crown, Terminal, Terminal retracement;
- entry ratio and `entry_level_untouched` decision;
- normalized Entry, Death, Stop, Target;
- risk distance, reward distance, realized R, volume;
- used-setup state, stable setup key, and runtime state key.

## Why a separate schema

A Phase 52 row has terminal Entry and F123 exit evidence. A Phase 55 row has projected Entry and attached fixed-R protection. Mixing them under one unlabeled row would corrupt analysis and restart audits.

Ledger routing follows the profile recovered from the already-owned broker exposure, not the operator's current input profile. Therefore restarting an 86.4 position while the input is temporarily set to Phase 52 cannot write that position into the wrong schema. Recovered pending/position rows include actual broker Entry, SL, TP, risk, reward, and realized R where available.

## Reason-code discipline

Every rejection is explicit, including configuration drift, canonical cycle/terminal/node failure, late level, geometry, quote/broker limits, duplicate exposure, persistent usage, volume, lock, send, or position protection failure.

## Reproducibility

A reviewer can recompute the raw 86.4 level from Crown and Origin, compare it to normalized Entry, recompute risk/target, and verify that the Terminal had not consumed the level at decision time.
