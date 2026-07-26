# Delayed Rebound Post F3 Hook

A Delayed/Rebound Post-F3 Hook appears after price reaches the F3 terminal side, moves away, and then forms the intended Hook slightly later.

This covers the user-described case:

```text
F3 side is hit
price rebounds upward
then a small Hook forms higher
```

## Why it matters

The intended Hook after F3 is not always born exactly at the F3 terminal endpoint.

Sometimes the direct terminal attempt does not complete, but the next rebound-cycle is the meaningful Hook.

## Versions

1. Delayed structural Hook: full nodes/sequences/confirmed terminal.
2. Delayed geometric 80% Hook: semicircle/cycle over threshold without full structural sequence.
