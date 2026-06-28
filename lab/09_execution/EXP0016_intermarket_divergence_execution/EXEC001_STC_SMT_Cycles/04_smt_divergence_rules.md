# 04 - SMT Divergence Rules

## 1. Domain

Divergence is defined only between two configured symbols:

```text
Symbol1
Symbol2
```

The strategy does not use broad market context, chart symbol, chart timeframe, or previous-day retained state.

## 2. Reference W levels

A reference W level is:

```text
Reference W High
Reference W Low
```

from an eligible W cycle inside the same M cycle.

## 3. Hunt rule

A hunt is touch-only.

### Low hunt

```text
bar.low <= reference_w_low
```

### High hunt

```text
bar.high >= reference_w_high
```

No candle close is required.

## 4. Raw bullish SMT divergence

A raw bullish SMT divergence forms when:

1. One symbol hunts an eligible reference W low.
2. The other symbol does not hunt the corresponding eligible reference W low.
3. The hunted and clean symbols belong to the same two-symbol pair.
4. The active W is not being compared with itself.
5. The reference W is inside the same M cycle.

Trade direction after confirmation:

```text
BUY clean_symbol
```

## 5. Raw bearish SMT divergence

A raw bearish SMT divergence forms when:

1. One symbol hunts an eligible reference W high.
2. The other symbol does not hunt the corresponding eligible reference W high.
3. The hunted and clean symbols belong to the same two-symbol pair.
4. The active W is not being compared with itself.
5. The reference W is inside the same M cycle.

Trade direction after confirmation:

```text
SELL clean_symbol
```

## 6. Confirmation rule

After raw divergence formation:

1. Create a pending divergence record.
2. Wait for the selected check candle to close.
3. At close, recompute whether the divergence is still true.
4. If it is still true, enter immediately.
5. If it is not true, cancel the pending divergence.

## 7. Divergence disappearance

A divergence disappears when the clean symbol also hunts the same-side corresponding reference level before check-candle close.

Example:

```text
SPX hunts reference low.
NDX has not hunted reference low.
Raw bullish divergence exists.
Before check candle closes, NDX also touches its reference low.
Divergence is canceled.
No entry.
```

## 8. Simultaneous opposite divergences

If buy and sell divergences are confirmed at the same time:

```text
No trade.
```

This is a hard skip condition in the source SRS.

## 9. One trade per divergence

A confirmed divergence can only generate one entry.

If the same divergence condition remains valid after the first entry:

```text
No re-entry.
```

## 10. W comparison matrix - literal source

The source SRS prints this matrix:

```text
W2 <- W1
W1 or W3 <- W2
W1 or W2 or W4 <- W3
```

The same rule applies for M1, M2, and M3.

## 11. W comparison matrix - implementation ambiguity

The source also says:

```text
The current W is never compared with itself.
Only previous W cycles of the same M are compared.
```

This creates an ambiguity because the printed matrix can be read in more than one direction.

### Conservative implementation candidate

If "previous W only" is treated as the dominant rule:

| Current W | Eligible reference W |
| --- | --- |
| W1 | none |
| W2 | W1 |
| W3 | W1, W2 |
| W4 | W1, W2, W3 |

### Literal-matrix implementation candidate

If the printed arrows are treated literally, the exact direction must be defined by the strategy owner before coding.

## 12. Required decision before code

The implementation must not lock the W comparison engine until the exact reference matrix is confirmed.

Recommended input design:

```text
InpReferenceMatrixMode = PREVIOUS_ONLY / SRS_LITERAL / CUSTOM
```

This allows testing both interpretations without rewriting the engine.
