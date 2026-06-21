# H4 Deep Atomic Report + H6 Reversal Optionality

This release extends the official M0004 atomic/no-sample report without reintroducing M0002 samples or fake same-candle ordering.

## Contract

- `sampleCalls=0`
- `branchSamplesBuilt=0`
- `m0002Calls=0`
- `sequenceOrder=known_time_batch_sequence`
- events known on the same candle/time are simultaneous
- mixed reversal/continuation batches are ambiguous and skipped from transition statistics

## New H4 deep reports

### `DAL_D0010_ATOMIC_INFORMATION`
Reports information-theoretic Markov memory over pure known-time batches:

- label entropy
- conditional entropy
- mutual information in bits
- predictability gain
- chi-square
- odds ratio
- Yule Q

### `DAL_D0010_ATOMIC_RUN_DISTRIBUTION`
Reports the full run-length tail surface:

- p50, p75, p90, p95 run length for all/reversal/continuation
- share of reversal/continuation batches inside 5+ and 10+ length runs

### `DAL_D0010_ATOMIC_BATCH_INTENSITY`
Reports same-time batch intensity and direction structure:

- mean event count per batch by regime
- multi-event batch percentage
- 3+ event batch percentage
- p90 event count
- buy/sell/no-dominant direction percentages

## New H6 report

### Hypothesis

`H0006_REVERSAL_EXPLOSIVE_OPTIONALITY`

The hypothesis is not that reversal has higher win rate. It tests whether reversal-known-time batches are stronger optionality points: points that produce fatter future excursion tails and more extreme movement potential than continuation batches.

### `DAL_H0006_OPTIONALITY_FAST/MAIN/SLOW`
For each pure known-time batch, measure future excursion only after the known time. Metrics are normalized by ATR at the known candle.

Outputs include:

- absolute optionality excursion in ATR
- directional MFE in batch direction
- adverse excursion
- p90/p95/p99 tail levels
- hit rates above configurable ATR thresholds
- top 10% tail share
- reversal-vs-continuation ratios and verdict

### `DAL_H0006_OPTIONALITY_STRESS_FAST/MAIN/SLOW`
A label-shuffle null that keeps future excursions fixed at the same known times and shuffles only the regime labels.

This asks whether reversal labels are statistically associated with higher optionality tails, not whether the market has high volatility in general.

## Inputs

- `InpAtomicPrintDeepReport`
- `InpAtomicPrintH6OptionalityReport`
- `InpAtomicStressH6Optionality`
- `InpH6HorizonBarsFast`
- `InpH6HorizonBarsMain`
- `InpH6HorizonBarsSlow`
- `InpH6AtrPeriod`
- `InpH6TailAtr1`
- `InpH6TailAtr2`
- `InpH6TailAtr3`

