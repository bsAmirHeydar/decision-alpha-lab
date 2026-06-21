# H0006 standalone optionality and edge-map report

H0006 is separated from H0004. H0004 remains the regime-memory hypothesis. H0006 tests a different question:

> Are reversal known-time batches better optionality points for future explosive movement, independent of ordinary win-rate?

The standalone expert is:

```text
mql5/Experts/DecisionAlphaLab/M0006/M0006_ReversalExplosiveOptionality.mq5
```

It uses the same atomic no-sample known-time batch contract as H0004:

```text
sampleCalls=0
branchSamplesBuilt=0
m0002Calls=0
sameKnownTimeEventsAreSimultaneous=1
mixedEnergyBatchPolicy=ambiguous_skip_from_transition
```

## Reports

`DAL_H0006_OPTIONALITY_FAST/MAIN/SLOW` compare reversal and continuation batches by future ATR-normalized movement after the known-time candle.

The report does not claim win-rate. It measures optionality:

- absolute future excursion in ATR units
- directional MFE in ATR units
- adverse excursion in ATR units
- p90 / p95 / p99 tails
- hit rates above configurable ATR thresholds
- top 10% tail concentration
- shuffle-label null stress

`DAL_H0006_EDGE_BUCKET_FAST/MAIN/SLOW` is the edge-map layer. It asks which sub-conditions are materially edge-like and which are unimportant.

Buckets include:

- `REV_ALL`, `CONT_ALL`
- single-event vs multi-event vs 3+ event batches
- dominant buy/sell direction
- start of regime run vs continuation of a regime run

Each bucket prints:

- `n` and `pctOfValid`
- `absMeanATR`, `absP75ATR`, `absP90ATR`, `absP95ATR`, `absP99ATR`
- hit rates over the configured tail ATR thresholds
- top 10% share
- p95/p99/hit-rate lift versus all batches
- `edgeScore`
- `materiality`

## Materiality labels

`too_sparse` means the bucket does not have enough observations.

`edge_candidate` means the bucket has positive tail lift and positive threshold-hit lift versus all batches.

`strong_edge_candidate` means the tail lift is large enough to deserve follow-up.

`negative_or_unimportant` means the bucket is weaker than the unconditional batch population.

## Why this exists

H0004 tells us whether branch labels have regime memory. H0006 tells us whether a subset of those known-time states is worth treating as an option-like location: rare, asymmetric, and capable of producing unusually large movement.
