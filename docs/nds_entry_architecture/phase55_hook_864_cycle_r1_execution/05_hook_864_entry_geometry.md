# 05 — Hook 86.4 Entry Geometry

## Canonical coordinates

The level is measured from Cycle Crown toward Hook Origin:

```text
EntryRaw = Crown + 0.864 × (Origin − Crown)
```

The same formula applies to both directions.

### Positive Hook / Buy Limit

```text
Origin < Entry86.4 < Crown
```

Example:

```text
Origin = 100
Crown  = 200
Entry  = 200 + 0.864 × (100 − 200) = 113.6
```

The order is a Buy Limit, so current Ask must remain above the normalized entry by the broker-required distance.

### Negative Hook / Sell Limit

```text
Crown < Entry86.4 < Origin
```

Example:

```text
Origin = 200
Crown  = 100
Entry  = 100 + 0.864 × (200 − 100) = 186.4
```

The order is a Sell Limit, so current Bid must remain below the normalized entry by the broker-required distance.

## Raw versus normalized price

The formula produces raw structural geometry. `FP_NDSHookTradeNormalizePrice` then aligns it to the symbol tick size:

- Buy entry rounds down, avoiding a higher-than-approved retracement price.
- Sell entry rounds up, avoiding a lower-than-approved retracement price.

## No terminal substitution

Phase 52 enters at `resolve_price`. Phase 55 records that Terminal only as eligibility/evidence; it enters at the 86.4 projection. The Hook detector and Terminal definition are not changed.
