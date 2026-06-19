# H0002 — Reversal vs Continuation Node-Exit Volatility Model

Status: active / fact-layer validation

## Research question

Given a valid completed M0001 structural-node event, does the completed exit side create different volatility regimes?

## Event source

H0002 uses the exact event stream created by H0001/M0001. It does not create a separate event builder.

A valid H0002 sample must be:

```text
closed = true
touch_confirmed = true
rtv_ready = true
entry_time >= analysis_start
```

The node lifecycle, hunt/touch consume behavior, revisit reset, baseline logic, warmup handling, and exit-gap logic are inherited from M0001.

## Exit logic

The M0001 event exit is side-agnostic. A completed exit candle can be fully above or fully below the frozen event territory.

```text
fully above frozen zone: bar.low  > event_upper
fully below frozen zone: bar.high < event_lower
```

The touch is confirmed only after `exit_gap` consecutive fully-outside candles. Exit is not equal to reversal.

## Branch classifier

At the completed exit candle:

```text
LOW node:
  close > node_price => REVERSAL_AFTER_EXIT
  close < node_price => CONTINUATION_AFTER_EXIT

HIGH node:
  close < node_price => REVERSAL_AFTER_EXIT
  close > node_price => CONTINUATION_AFTER_EXIT
```

## Measurement

The primary measurement is locked to the original M0001 event RTV:

```text
branchRTV = event.rtv
branchLog = log(event.rtv)
```

The branch label must not change the sample window.

## Current working model

The branch model is not only a comparison of two means. It has four observed dimensions:

### 1. Frequency

Reversal tends to be more common; continuation tends to be less common.

Observed working pattern:

```text
reversal:continuation ≈ 1.6:1 to 2:1
```

### 2. Intensity

Continuation tends to show higher event RTV intensity:

```text
continuation logMean > reversal logMean
continuation rawMean > reversal rawMean
continuation vsRandomGeoRatio > reversal vsRandomGeoRatio
```

### 3. Tail

Continuation tends to carry a heavier right tail:

```text
continuation P90/P95/CVaR90/CVaR95 > reversal P90/P95/CVaR90/CVaR95
```

### 4. Post-event memory

Continuation tends to preserve higher post-event volatility across configured horizons:

```text
continuation h5/h10/h20/h50 DLog > reversal h5/h10/h20/h50 DLog
```

## Acceptance signature

H0002 is strongly supported when the same pattern appears across markets/timeframes:

```text
frequencyModel = reversal_higher_frequency_continuation_lower_frequency
intensityModel = continuation_higher_event_rtv_intensity
tailModel = continuation_fatter_right_tail
persistenceModel = continuation_higher_post_event_volatility_persistence
```

The strongest compact conclusion is:

```text
combinedModel = continuation_lower_frequency_higher_intensity_higher_persistence_fatter_tail
```

## Interpretation

H0002 is not a directional entry rule. It is a volatility-regime classifier:

```text
Reversal branch: more common, lower intensity.
Continuation branch: less common, higher intensity, stronger volatility memory, fatter tail.
```

Future strategy work may use this branch model as a quality or volatility-intensity filter, but that is separate from validating the fact layer.
