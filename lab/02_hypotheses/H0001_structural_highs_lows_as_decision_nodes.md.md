---
id: H0001
status: draft

origin_observations:
  - OBS0001

related_experiments: []
related_validations: []
related_signals: []

created: 2026-06-12
owner: Decision Alpha Lab
priority: critical
---

# H0001 — Structural Highs and Lows as Decision Nodes

## Status

Draft

---

## Research Question

Do structurally defined highs and lows contain statistically distinguishable information about subsequent market behavior compared to arbitrary price locations?

---

## Background

OBS0001 documented a recurring practical observation:

Trading approaches that ignored structural highs and lows generally exhibited poor performance, whereas approaches that explicitly incorporated these structures often demonstrated improved outcomes.

In addition, market behavior observed around these locations appeared qualitatively different.

Observed differences included:

- changes in movement speed,
- temporary stalling or congestion,
- abrupt and forceful breakouts,
- unequal persistence following breaks,
- asymmetry in subsequent behavior.

These observations motivate formal investigation.

---

## Hypothesis

Structurally defined highs and lows are not equivalent to arbitrary price locations.

They represent privileged regions of market interaction where subsequent price behavior exhibits statistically distinguishable characteristics.

For the purpose of this research program, these regions are provisionally referred to as "decision nodes."

---

## Null Hypothesis (H0)

Subsequent market behavior around structurally defined highs and lows is statistically indistinguishable from behavior observed around randomly selected price locations.

Any apparent differences arise from randomness, selection bias, data mining, or subjective interpretation.

---

## Alternative Hypothesis (H1)

Subsequent market behavior around structurally defined highs and lows differs significantly from behavior observed around randomly selected price locations.

These differences reflect measurable structural information embedded in market behavior.

---

## Operational Definition

A structural high or low must be extracted using explicit and reproducible rules.

Candidate extraction methods include:

- Pivot (2 bars left, 2 bars right),
- Five-bar fractals,
- Adaptive structural pivots,
- Alternative rule-based definitions.

Support for this hypothesis must not depend exclusively on one extraction method.

---

## Expected Observable Differences

If the hypothesis is true, one or more of the following characteristics should differ between structural nodes and random locations:

### Movement Characteristics

- Movement speed after interaction,
- Acceleration or deceleration patterns,
- Breakout velocity.

### Interaction Characteristics

- Frequency of rejection,
- Duration of congestion,
- Number of retests,
- Time spent near the level.

### Break Characteristics

- Breakout frequency,
- Breakout persistence,
- False breakout frequency,
- Post-break continuation.

### Structural Characteristics

- Pullback depth,
- Pullback duration,
- Directional asymmetry following interaction.

---

## Statistical Expectations

Evidence supporting this hypothesis should satisfy the following conditions:

- Effects should be observable out-of-sample.
- Effects should persist across multiple market periods.
- Effects should not vanish under small parameter changes.
- Effects should outperform appropriate random baselines.

---

## Failure Conditions

This hypothesis should be rejected if:

- No statistically meaningful differences are detected.
- Similar effects are observed around random locations.
- Observed effects disappear out-of-sample.
- Results depend entirely on parameter tuning.
- The phenomenon cannot be reproduced independently.

---

## Implications if Supported

Support for this hypothesis would justify investigation into:

- H0002: Node heterogeneity,
- H0003: Quantification of node energy,
- H0004: Regime transition detection,
- H0005: Alpha extraction from structural information.

---

## Implications if Rejected

Rejection of this hypothesis would undermine the assumption that structural highs and lows constitute privileged market regions.

The broader research program based upon this assumption should be reconsidered or reformulated.

---

## Notes

Acceptance of this hypothesis does not imply predictive certainty.

It only implies that structural highs and lows contain information not present in arbitrary locations.

The economic usefulness of such information remains a separate question requiring independent investigation.