# Cycle-End Time Target Doctrine

## Definition

The target is not a price target.

The target is the end of the current cycle in the cycle group that generated the signal.

Example:

```text
cg_180m signal in 21:00–23:59 cycle
scheduled target exit = 23:59 / cycle end
```

## Runtime meaning

The EA must close the position at or immediately after the scheduled cycle end.

This creates a time-based lifecycle:

```text
entry after candle close
stop at clean reference level
exit at CG cycle end unless stopped first
```

## Implementation implication

The trade router cannot rely only on broker TP. It needs a position manager that checks time and closes expired positions.

