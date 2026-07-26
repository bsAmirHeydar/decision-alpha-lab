# H0002 — Structural Node Territories and Revisitation Dynamics

## Status

Draft

---

## Motivation

H0001 proposed that structurally defined highs and lows may represent privileged regions of market interaction rather than arbitrary price locations.

However, H0001 did not specify how such structural locations should be revisited and evaluated after their initial formation.

A common assumption among discretionary traders is that previously established structural highs and lows continue to influence market behavior when revisited. These locations are often described as areas where the market "remembers" prior interactions.

This assumption remains largely anecdotal.

The present hypothesis aims to formalize this intuition into an explicit and testable framework.

Rather than treating structural nodes as infinitesimal price points, this framework treats them as territories with finite influence and a definable lifecycle.

The central question becomes:

> Do confirmed structural nodes continue to exhibit distinguishable behavioral effects when revisited by price, and if so, under what conditions do these effects cease to exist?

---

# Research Question

Do previously confirmed structural highs and lows exhibit statistically distinguishable market reactions upon revisitation compared to arbitrary price locations?

Furthermore:

* How should the effective territory of a structural node be defined?
* When does a structural node cease to exert influence?
* Is the first revisit unique, or does the node remain active until invalidation?

---

# Conceptual Framework

A structural node is assumed to evolve through multiple stages rather than existing as a static event.

Instead of viewing a node as a single price level, the node is modeled as an object possessing:

* formation,
* confirmation,
* expansion,
* territory,
* revisitation,
* consumption,
* termination.

This lifecycle provides an operational basis for quantitative investigation.

---

# Structural Node Lifecycle

Each node progresses through the following stages:

## 1. Creation

A candidate structural high or low is identified using explicit extraction rules.

Examples include:

* L-rule pivots,
* fractals,
* alternative structural definitions.

Only rule-based and reproducible methods are permitted.

---

## 2. Confirmation

The node becomes confirmed once the required future conditions are satisfied according to the extraction method.

Only confirmed nodes participate in this study.

Unconfirmed nodes are excluded.

---

## 3. Expansion

After confirmation, price moves away from the node.

This movement determines the node's effective scale.

For a Low Node:

* Node Price = N
* Expansion Extreme = highest price reached after confirmation and before revisitation.

For a High Node:

* Node Price = N
* Expansion Extreme = lowest price reached after confirmation and before revisitation.

The expansion phase defines the magnitude of the node's influence.

---

# Territory Definition

A node is assumed to possess a finite territory rather than a single actionable price.

Territory width is derived from the node's expansion.

Let:

For Low Nodes:

Range = ExpansionExtreme − NodePrice

For High Nodes:

Range = NodePrice − ExpansionExtreme

A parameter:

Territory Parameter = Z

is introduced.

Example:

Z = 0.80

implies that the inner 80% nearest the node constitutes its territory.

---

## Low Node Example

Node:

100

Expansion Extreme:

150

Range:

50

Territory Half Width:

50 × (1 − 0.80)

= 10

Therefore:

Territory = [90, 110]

Price entering this region is interpreted as a revisitation of the node.

---

## High Node Example

Node:

150

Expansion Extreme:

100

Range:

50

Territory Half Width:

10

Therefore:

Territory = [140, 160]

Entry into this interval constitutes revisitation.

---

# Revisitation Event

A revisitation event occurs when price enters the territory of a previously confirmed node.

The event begins at the first moment price crosses into the territory.

The objective is to observe whether such events exhibit behavioral characteristics distinguishable from random baselines.

---

# Node Consumption Models

Two alternative assumptions are proposed.

These represent competing hypotheses regarding structural memory.

---

## Model A — Hunt Consumption

A node remains active until it is explicitly violated.

For Low Nodes:

Node Death Condition:

Price < Node Price

For High Nodes:

Node Death Condition:

Price > Node Price

Until such violation occurs:

* the node remains alive,
* multiple revisitations are possible,
* multiple reactions may be recorded.

Interpretation:

> Structural influence persists until the underlying liquidity associated with the node is consumed.

---

## Model B — First-Touch Consumption

A node is considered exhausted immediately upon its first revisitation.

Once price enters the territory:

* the node is marked as consumed,
* no future revisitations are considered,
* subsequent interactions are ignored.

Interpretation:

> Structural memory is released only once.

---

# Competing Assumptions

These models imply fundamentally different views of market structure.

Model A assumes:

> structural memory persists until invalidation.

Model B assumes:

> structural memory dissipates upon first access.

The relative explanatory power of these models constitutes a research question in its own right.

---

# Observable Behaviors

The current objective is not alpha generation.

Instead, the goal is to determine whether revisitations exhibit non-random characteristics.

Candidate observations include:

* reaction intensity,
* volatility clustering,
* unusually small reactions,
* unusually large reactions,
* persistence within territory,
* termination characteristics.

Directional profitability is explicitly excluded from the initial investigation.

---

# Null Hypothesis

Market behavior observed during revisitations of confirmed structural node territories is statistically indistinguishable from behavior observed at comparable random locations.

Any apparent effects arise from chance, selection bias, or data-mining artifacts.

---

# Alternative Hypothesis

Revisitations of confirmed structural node territories exhibit statistically distinguishable characteristics relative to random baselines.

These differences reflect persistent structural information embedded within market behavior.

---

# Failure Conditions

This hypothesis should be rejected if:

* no reproducible differences emerge,
* effects disappear out-of-sample,
* results depend entirely on parameter tuning,
* random baselines exhibit equivalent behavior,
* findings cannot be independently replicated.

---

# Implications if Supported

Support for this hypothesis would suggest that structural nodes possess measurable memory extending beyond their initial formation.

This would justify further investigation into:

* node state transitions,
* node strength estimation,
* node heterogeneity,
* reaction classification,
* structural alpha extraction.

---

# Implications if Rejected

Failure to support this hypothesis would challenge the assumption that confirmed structural nodes retain informational significance after formation.

The notion of persistent structural memory would require reconsideration or abandonment.

---

# Notes

Acceptance of this hypothesis does not imply predictive certainty.

It does not establish profitability.

It only implies that previously confirmed structural nodes behave differently from arbitrary market locations when revisited.

Whether such differences possess economic value remains a separate empirical question.
