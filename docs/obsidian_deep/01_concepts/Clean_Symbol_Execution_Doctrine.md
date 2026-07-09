# Clean Symbol Execution Doctrine

## Definition

The clean symbol is the symbol that did not hunt the reference level.

If Symbol A hunts and Symbol B does not:

```text
hunter = A
clean = B
trade = B
```

If Symbol B hunts and Symbol A does not:

```text
hunter = B
clean = A
trade = A
```

## Bullish divergence

Low-side asymmetry:

```text
one symbol hunts reference low
other symbol does not
=> buy clean symbol
```

Stop:

```text
clean symbol reference low
```

## Bearish divergence

High-side asymmetry:

```text
one symbol hunts reference high
other symbol does not
=> sell clean symbol
```

Stop:

```text
clean symbol reference high
```

## Why this matters

The model does not chase the instrument that already performed the liquidity hunt. It positions on the instrument that stayed clean relative to its own reference level.

