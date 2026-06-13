# M0001 — Relative Territory Volatility (RTV)

## Status

Draft

Associated Hypothesis:

* H0002 — Structural Node Territories and Revisitation Dynamics

---

# Objective

The objective of this metric is to determine whether market volatility changes systematically when price revisits previously confirmed structural nodes.

More specifically:

> Does market activity inside structural node territories exhibit different volatility characteristics compared to the market's immediately preceding behavior?

This metric does not attempt to predict direction, profitability, or alpha.

Its sole purpose is to determine whether revisitations of structural territories coincide with statistically distinguishable volatility regimes.

---

# Motivation

A common discretionary belief is that previously established structural highs and lows remain behaviorally important when revisited.

Traders often describe these regions as:

* areas of decision,
* liquidity interaction zones,
* regions of conflict,
* zones of increased activity.

If such intuition is valid, then volatility observed during revisitations should differ from volatility observed immediately before revisitation.

The present metric formalizes this intuition.

---

# Scope

This metric applies exclusively to:

* confirmed structural nodes,
* nodes possessing a valid territory,
* revisitation events defined under H0002.

Unconfirmed nodes are excluded.

---

# Definitions

## Structural Node

A previously confirmed structural high or low.

Examples include:

* L-rule pivots,
* fractals,
* alternative rule-based node definitions.

The extraction method is independent of this metric.

---

## Territory

The finite region surrounding a structural node defined according to H0002.

Example:

Low Node:

Node Price:

100

Expansion Extreme:

150

Range:

50

Territory Parameter:

0.80

Half Width:

50 × (1 − 0.80)

= 10

Territory:

[90, 110]

---

# Revisitation Event

A revisitation event begins when price first enters the territory.

Entry detection uses intrabar extremes.

For Low Nodes:

Entry occurs when:

Low ≤ Territory Upper Boundary

For High Nodes:

Entry occurs when:

High ≥ Territory Lower Boundary

Open and Close prices are ignored for event detection.

Only High and Low values are considered.

---

# Event Termination

Event termination depends on the selected consumption model.

---

## First-Touch Consumption

The event ends immediately after the first territory interaction.

The node is permanently removed from future consideration.

---

## Hunt Consumption

The node remains active until invalidation.

Low Nodes terminate when:

Low < Node Price

High Nodes terminate when:

High > Node Price

Multiple revisitations are therefore possible.

---

# Event Length

Let:

N

denote the number of candles comprising the revisitation event.

Because territory interactions naturally vary in duration:

* N may equal 2,
* N may equal 54,
* N may equal 120.

No fixed look-ahead window is imposed.

The market determines the event duration.

---

# Intrabar Volatility Measure

For each candle i within the event:

The intrabar logarithmic range is defined as:

r_i = ln(High_i / Low_i)

Properties:

* scale invariant,
* direction independent,
* comparable across assets,
* incorporates wick activity,
* robust to differences in absolute price level.

This quantity represents the magnitude of price exploration within the candle.

---

# Territory Volatility

The average intrabar logarithmic volatility inside the revisitation event is defined as:

V_zone

V_zone =
(1 / N)
×
Σ r_i

where the summation spans all candles belonging to the revisitation event.

Explicitly:

V_zone =
(1 / N)
×
Σ ln(High_i / Low_i)

for i = 1 to N.

---

# Baseline Volatility

To construct a self-normalized comparison:

The N candles immediately preceding territory entry are selected.

These candles form the baseline period.

Let:

V_base

denote the average logarithmic intrabar volatility over this baseline.

V_base =
(1 / N)
×
Σ ln(High_i / Low_i)

computed over the N candles prior to entry.

---

# Relative Territory Volatility

The Relative Territory Volatility ratio is defined as:

RTV =
V_zone / V_base

This ratio constitutes the primary output of M0001.

---

# Interpretation

RTV ≈ 1

Market behavior inside the territory is indistinguishable from immediately preceding behavior.

No evidence of a volatility regime shift.

---

RTV > 1

Volatility inside the territory exceeds baseline volatility.

The revisitation event coincides with intensified market activity.

Examples:

* aggressive reactions,
* stop runs,
* impulsive responses,
* conflict-driven expansions.

---

RTV < 1

Volatility inside the territory is lower than baseline volatility.

The revisitation event coincides with relative suppression of activity.

Examples:

* absorption,
* hesitation,
* equilibrium,
* passive interaction.

---

# Statistical Interpretation

Under the null hypothesis:

The distribution of RTV values observed during structural revisitations should be indistinguishable from RTV values obtained from random baselines.

Formally:

RTV_structural

≈

RTV_random

Any deviations are attributed to randomness.

---

Under the alternative hypothesis:

RTV_structural

≠

RTV_random

indicating that structural territories are associated with distinct volatility dynamics.

---

# Random Baseline

To evaluate statistical significance:

Random pseudo-events should be generated.

Each pseudo-event should match:

* event duration N,
* market period,
* asset,
* timeframe.

RTV values from structural revisitations are then compared against RTV values from random revisitations.

Candidate comparison methods include:

* bootstrap procedures,
* permutation testing,
* Mann–Whitney U tests,
* Kolmogorov–Smirnov tests.

The choice of test is independent of the metric definition.

---

# Outputs

For each revisitation event, the following fields should be recorded:

* node_id,
* node_type,
* node_price,
* territory_entry_time,
* territory_exit_time,
* event_length_N,
* V_zone,
* V_base,
* RTV,
* consumption_mode.

These observations collectively form the empirical dataset used to evaluate H0002.

---

# Notes

M0001 intentionally avoids:

* directional assumptions,
* profitability measures,
* predictive claims,
* alpha estimation.

It addresses a narrower question:

> Does the market exhibit different volatility behavior when interacting with previously confirmed structural territories?

Only after establishing the existence of such differences should further investigation into economic usefulness be pursued.
