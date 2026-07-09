# CG Intermarket Divergence MOC

## Identity

CG Intermarket Divergence is an independent expert architecture for detecting and trading two-symbol divergence inside configurable time cycle groups.

It is a clean framework for:

```text
symbol A vs symbol B
cycle-group reference high/low
touch-only hunt asymmetry
candle-close confirmation
clean-symbol execution
cycle-end time exit
```

## Canonical concepts

- [[Cycle Group Calendar Doctrine]]
- [[Touch-Only Hunt and Candle-Close Confirmation]]
- [[Clean Symbol Execution Doctrine]]
- [[Cycle-End Time Target Doctrine]]
- [[Same-Day Signal Boundary]]
- [[CG MQL5 Modular Architecture]]
- [[CG Implementation Checklist]]

## Hard rules

1. Trading day starts at 18:00 New York.
2. Trading day ends at 17:00 New York.
3. Hunt is touch-only.
4. Equal high/low is hunt.
5. Divergence exists only after candle close.
6. Low hunt asymmetry = bullish divergence.
7. High hunt asymmetry = bearish divergence.
8. Trade happens on non-hunter / clean symbol.
9. Stop is clean symbol reference level.
10. Exit target is current cycle end.
11. Risk is 1% of equity.
12. No previous-day data is needed for entry.

## Implementation status

This patch creates only the doctrine and architecture notes. Code follows in a later patch.

