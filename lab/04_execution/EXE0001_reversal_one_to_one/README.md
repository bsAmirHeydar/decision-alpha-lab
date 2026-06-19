# EXE0001 — Reversal One-to-One

Purpose: operationalize the H0005 reversal first-move edge with a simple fixed-R limit-order model.

## Inputs

- cash risk
- commission per 1 lot round-turn
- reward R multiple
- max simultaneous trades
- allow/disallow opposite-direction exposure

## Entry/exit

```text
BUY reversal:
  node type = LOW
  entry = upper edge of the structural zone
  stop  = lower edge of the structural zone
  tp    = entry + rewardR * (entry - stop)

SELL reversal:
  node type = HIGH
  entry = lower edge of the structural zone
  stop  = upper edge of the structural zone
  tp    = entry - rewardR * (stop - entry)
```

## Scope

This module is a first execution template. It does not include spread/slippage modeling beyond the explicit commission input. It should be run in dry-run mode first and then tested in Strategy Tester before live use.
