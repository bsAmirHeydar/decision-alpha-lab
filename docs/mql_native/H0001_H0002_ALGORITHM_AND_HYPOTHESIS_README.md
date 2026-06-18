# H0001 / H0002 Algorithm and Hypothesis README

Version: 1.73

This document is the logic lock for the first two Decision Alpha Lab hypotheses. It is written as a research README, not as a strategy guide. The goal is to make every algorithmic assumption explicit enough that future reports can be audited against it.

## Current research stack

```text
H0001 / M0001: Structural node territory events have higher relative volatility than matched random windows.
H0002 / M0002: Completed node events have two branch regimes: reversal exit and continuation exit. The branches differ in frequency, intensity, tail behavior, and post-event volatility persistence.
```

M0002 does not create a separate event stream. It receives the exact completed events produced by M0001 and only labels them by the side of the completed exit candle relative to the original node price.

## H0001 — Structural node relative territory volatility

### Research question

Do rule-based structural highs/lows produce higher event-window volatility than matched random windows?

### Structural nodes

A node is defined by the L-rule. The pivot candle is the visual marker, but logic starts only after the right-side confirmation exists.

```text
HIGH node: high[i] >= max(left L highs) and high[i] >= max(right L highs)
LOW node:  low[i]  <= min(left L lows)  and low[i]  <= min(right L lows)

active_from_index = node_index + L
```

No event may start before `active_from_index`. This is the lookahead guard.

### Live territory construction

The node price is the anchor. The live expansion extreme updates while the node is alive.

```text
LOW node:  tracking_extreme = highest high after active_from
HIGH node: tracking_extreme = lowest low after active_from
```

Territory is built around the original node price:

```text
distance = abs(tracking_extreme - node_price)
half_width = distance * (1 - zone_ratio)

territory_lower = node_price - half_width
territory_upper = node_price + half_width
```

### Touch event

A touch event starts when a candle intersects the current live territory:

```text
bar.low <= territory_upper and bar.high >= territory_lower
```

At entry, the geometry freezes:

```text
event_lower = live_lower at entry
event_upper = live_upper at entry
event_extreme = tracking_extreme at entry
```

After this point, the event exit test uses the frozen event zone, not the updating live zone.

### Exit logic

Exit is side-agnostic. It does not mean reversal. It only means the candle is fully outside the frozen event zone.

A candle is outside the event zone if it does not overlap the frozen zone:

```text
fully above zone: bar.low  > event_upper
fully below zone: bar.high < event_lower
```

A candle is not outside if any part of its high/low range overlaps the frozen zone.

The touch is confirmed when:

```text
outside_count >= exit_gap
```

Any candle that overlaps the frozen zone resets `outside_count` to zero.

### Consumption mode

Consumption is input-driven.

```text
CONSUME_BY_TOUCH:
  confirmed touch consumes the node.
  no later revisits are allowed.

CONSUME_BY_HUNT:
  confirmed touch does not consume the node unless a node break/hunt occurred during that completed event.
  if there was no hunt, the node remains alive and the next territory cycle is recomputed after the confirmed exit.
```

A node break before a territory touch consumes the node in HUNT mode. A node break during an event does not cancel that event; the event still must complete the normal exit-gap rule, and then the consume mode decides whether the node is consumed.

### RTV measurement

M0001 uses candle log-range volatility:

```text
log_move = abs(log(high / low))
```

The event sample is:

```text
inside = event entry through rtv_inside_end
```

The final `exit_gap` candles are excluded from inside RTV because they are exit-confirmation candles, not inside-event candles.

The baseline is the equal-length window immediately before event entry:

```text
mean_inside = mean(log_move over inside)
mean_before = mean(log_move over equal-length pre-entry baseline)
RTV = mean_inside / mean_before
logRTV = log(RTV)
```

### Random null model

The current random model is deterministic and reproducible:

```text
engine = hash32_v2_deterministic_uniform_entry
entryDistribution = uniform_over_valid_entry_indexes
baselineGuard = beforeRandomEntry
eventLengthMatched = 1
randomWindowsNotCountedAsEvents = 1
```

For each real event, random windows use the same sample length and an equal-length baseline before the random entry.

### H0001 acceptance pattern

H0001 is supported when node events beat matched random windows under the main report and the stress suite:

```text
NODES/RANDOM/COMPARE positive
HARD_NULL positive
PLACEBO near zero
OUTLIER_STRESS survives
NONOVERLAP remains positive
CLUSTER_ROBUST remains positive
BLOCK_BOOT CI positive
NEGATIVE_CONTROL near zero
```

## H0002 — Reversal vs continuation volatility model

### Research question

After a valid M0001 event completes its exit-gap rule, does the event belong to two different volatility regimes depending on whether the completed exit candle closes on the reversal side or continuation side of the original node price?

### Event source

H0002 uses only valid M0001 events:

```text
closed = true
touch_confirmed = true
rtv_ready = true
entry_time >= analysis_start
```

H0002 never builds a neutral repeated event stream and never measures a new primary window after the outcome candle.

### Branch classifier

The default outcome candle is the candle that completes the exit-gap rule:

```text
outcome_index = exit_index + InpOutcomeCandleOffsetAfterExit
```

Default:

```text
InpOutcomeCandleOffsetAfterExit = 0
```

Branch rule:

```text
LOW / valley node:
  close[outcome_index] > node_price => REVERSAL_AFTER_EXIT
  close[outcome_index] < node_price => CONTINUATION_AFTER_EXIT

HIGH / peak node:
  close[outcome_index] < node_price => REVERSAL_AFTER_EXIT
  close[outcome_index] > node_price => CONTINUATION_AFTER_EXIT
```

If the close equals the node price, the sample is `UNKNOWN` and excluded from branch comparison.

### Primary measurement

The branch label does not change the volatility window.

```text
branchRTV = event.rtv
branchLog = log(event.rtv)
```

So H0002 asks: among the same exact M0001 event-window RTV values, how does volatility differ between reversal exits and continuation exits?

### H0002 model dimensions

The observed branch model should be evaluated through several separate dimensions.

#### 1. Frequency / count model

The repeated pattern so far is that reversal exits are more frequent, while continuation exits are less frequent.

Typical observed structure:

```text
reversal share:     about 60% to 66%
continuation share: about 34% to 40%
reversal:continuation count ratio: roughly 1.6:1 to 2:1
```

Interpretation:

```text
Continuation is lower-frequency.
Reversal is higher-frequency.
```

#### 2. Event intensity model

Continuation exits have repeatedly shown higher event RTV intensity.

Core measures:

```text
continuation logMean > reversal logMean
continuation rawMean > reversal rawMean
continuation rawMedian often > reversal rawMedian
continuation pairedWin vs random > reversal pairedWin vs random
continuation CohenD vs random > reversal CohenD vs random
```

Interpretation:

```text
Continuation is lower-frequency but higher-intensity.
```

#### 3. Tail model

Continuation often has heavier upper-tail volatility.

Core measures:

```text
continuation rawP90 / rawP95 / CVaR90 / CVaR95
vs
reversal rawP90 / rawP95 / CVaR90 / CVaR95
```

Interpretation:

```text
Continuation is more likely to carry tail-risk / tail-opportunity.
```

#### 4. Post-event volatility memory model

Continuation also appears to preserve higher volatility after the completed event.

Core measures:

```text
CONTINUATION_AFTER_EXIT_HORIZON h5/h10/h20/h50
vs
REVERSAL_AFTER_EXIT_HORIZON h5/h10/h20/h50
```

The current working sub-hypothesis is:

```text
Continuation exit creates stronger post-event volatility persistence than reversal exit.
```

#### 5. Locality / placebo model

Placebo shifts test whether the signal is local to the true node or just a broad regime artifact.

Ideal pattern:

```text
main branch effect strong
placebo plus/minus near zero
negative control random-vs-random near zero
```

If one placebo side stays positive, the interpretation is not automatic failure. It may indicate a broader volatility regime memory around node neighborhoods. That case requires multi-shift placebo tests.

## New M0002 branch model report

Version 1.73 adds a compact branch-level model line:

```text
DAL_M0002_FINAL_BRANCH_MODEL
```

It summarizes:

```text
frequencyModel
reversalToContinuationCountRatio
continuationToReversalCountRatio
intensityModel
contOverRevGeoMeanRatio
contOverRevRawMeanRatio
contOverRevRawMedianRatio
tailModel
contOverRevP95Ratio
contOverRevCVaR95Ratio
persistenceModel
horizon continuation-vs-reversal deltas
combinedModel
```

The desired high-quality H2 signature is:

```text
combinedModel = continuation_lower_frequency_higher_intensity_higher_persistence_fatter_tail
```

This means the branch is not merely a yes/no reversal-vs-continuation label. It is a volatility regime classifier.

## Code invariants checked in v1.73

```text
M0001 exit is side-agnostic: exit can complete above or below frozen territory.
M0001 does not cancel a pending touch just because the node price breaks during the event.
M0001 consume behavior is controlled by InpConsumeMode.
M0002 calls DAL_M0001ComputeEvents() and does not build a separate neutral event stream.
M0002 default measure mode is EVENT_RTV.
M0002 branch label uses close vs node_price at the completed exit candle.
M0002 branch label does not change sample_start, sample_length, or event RTV in production mode.
Random windows are event-length matched and are not counted as real events.
```

## Research interpretation

Current working interpretation:

```text
H0001: Structural node territory events are volatility expansion zones.
H0002: Continuation exits are lower-frequency but higher-volatility branch outcomes.
H0002-B: Continuation exits preserve stronger post-event volatility memory.
H0002-C: Continuation exits carry a fatter upper-tail volatility profile.
```

These are not yet directional entry rules. They are fact-layer hypotheses. Strategy design should come only after cross-market, cross-timeframe, multi-shift placebo, and seed-ensemble random validation.
