# SCN-R01 — Normalized Interpretation

## Core Claim

The correct model is not only `context_power`.

The correct model is:

```text
Context → Position → Constraint → Zone → Entry
```

Power matters, but power alone is insufficient.

The system must first identify the structural position, then identify the exploitable constraints inside that position, then evaluate whether those constraints offer favorable cost/reward.

Suggested core object:

```text
PositionConstraint
```

This means NDS should not ask only:

```text
how strong is this context?
```

It should ask:

```text
where are we?
what constraints exist here?
which constraints can be exploited with low cost and high reward?
which state interpretation is cheapest and most profitable to trade?
```

## Two Main Training Targets

The user defined two main training domains.

### Training Target 1 — Exploitable Movement Constraint

Question:

```text
Which movement constraint is exploitable with lower cost?
```

Meaning:

```text
lower risk
higher reward
longer profit path
better optionality
```

This is a reward-first / convexity-first context model.

The model should learn which NDS constraints produce the best cost-to-potential profile.

### Training Target 2 — Multi-State Policy Choice

Some parts of NDS are already fixed.

Other parts are two-state or multi-state.

When no single deterministic rule exists, training should determine:

```text
which state interpretations should be considered
which ones cost less
which ones produce more reward
which ones should be ignored or vetoed
```

This is not ontology learning.

It is policy learning over NDS-native states.

## Fixed Anatomy vs Learnable Policy

### Fixed NDS Anatomy

These are structural and should not be redefined by AI:

```text
Hook
Rally
CycleHook
Node
Sequence
X closure
Y closure
Symmetry
ND
Destination
Parent/child scale
Context / zone / entry hierarchy
```

### Learnable Policy

These should be trained:

```text
context power score
constraint exploitability
reversal probability proxy
zone precision from Y closure
symmetry usefulness
destination optionality value
which multi-state branch to act on
entry risk allocation
stepwise exit policy
```

## Context Is Position

Context is not merely a strength score.

Context means reading Hook and Rally in both bullish and bearish forms, across fractal scales, until the system understands its current position.

Position must include:

```text
bullish Hook/Rally state
bearish Hook/Rally state
parent context
current context
child refinement context
CycleHook state
X/Y closure state
destination state
open one-and-two structures
zone candidate
```

Only after position is known can a trade zone be considered.

## Three-Layer Decision Structure

The user explicitly defines three layers:

```text
1. Context
2. Zone
3. Entry
```

Context identifies the structural position.

Zone identifies the tradeable region created by constraints and confluence.

Entry is taken in a lower timeframe, usually with a reversal limit setup when inside that zone.

Therefore, context power must not be collapsed into entry quality.

## Constraint-Based Betting

The project is not betting on prediction.

It is betting on constraints.

The anatomy defines constraints such as:

```text
counting constraints
symmetry constraints
Hook constraints
CycleHook constraints
Rally constraints
levels that should not be hit
levels that should be hit
open one-and-two structures that expect a future three
ND / origin constraints
destination constraints
```

The model must score the strength and exploitability of the specific constraint being traded.

## X and Y Closure

### X Closure

Usually at least one X closure is needed for reversal power.

Interpretation:

```text
X closure is a minimum reversal-power condition.
```

This should become a strong feature or possible rule.

### Y Closure

Y closure helps define the reversal zone more accurately and shows momentary energy.

Interpretation:

```text
Y closure improves zone precision and local energy reading.
```

### XY Closure

When both X and Y are closed, reversal probability is higher.

Suggested labels:

```text
X_CLOSED_REVERSAL_POWER
Y_CLOSED_ZONE_PRECISION
XY_CLOSED_HIGHER_REVERSAL_PROBABILITY
```

## Multiple Sequence Closure

When multiple sequences close, context power increases.

This suggests a confluence model:

```text
more closed sequences
→ stronger constraint
→ stronger reversal context
→ better zone confidence
```

But exact weighting should be trained.

## Symmetry Confluence

Symmetry is not merely a nice shape.

When symmetry accumulates around a specific area, it can create:

```text
trading zone
entry-level Extreme
```

This creates a bridge:

```text
symmetry confluence → zone promotion
symmetry confluence at entry scale → Extreme entry refinement
```

This is central for `context_to_zone_promotion_policy_v1`.

## Destination and Open One-and-Twos

The user introduces an important destination concept:

```text
open one-and-twos
```

Meaning:

```text
the market will eventually come with a three and hit them,
but timing is unknown
```

This can be used as destination logic.

Important distinction:

```text
destination likelihood may be high
timing is uncertain
```

This means open one-and-twos are destination magnets, but not timing guarantees.

## Optionality

If destination or take-profit is too close, optionality is lower.

The system must evaluate whether the trade is worth taking.

Optionality depends on:

```text
distance to destination
number of available destinations
reward path openness
ability to scale out
risk of entry
ability to use multiple entries with different risk
```

This supports flexible execution:

```text
multiple entry points
different risk per entry
stepwise exits
multiple destinations
```

These flexibilities are allowed, but should be modeled and tested.

## Parent / Child Context

Higher timeframe is dominant.

Lower timeframe is not used to overthrow the higher timeframe by default.

Lower timeframe is used to see:

```text
how the higher-timeframe map is being carried out micro-structurally
```

Therefore:

```text
parent context = strategic map
child context = tactical execution/refinement
```

This is a hard architectural relationship.

## Weak Context

Weak context is not defined by one feature.

It is weak when the combined NDS grading is weak.

Possible weakness sources:

```text
no meaningful X closure
weak or absent Y precision
few closed sequences
no symmetry confluence
unclear Hook/Rally position
near destination / low optionality
parent-child conflict
weak constraint to bet on
no valid zone promotion
entry exists without context
```

## Output Model

The output should not be only a single number.

It should include:

```text
position state
constraint type
constraint strength
constraint exploitability
context power score
zone promotion state
destination optionality
entry permission
veto/watchlist/tradable status
```

Suggested classes:

```text
CONTEXT_ONLY
POSITION_IDENTIFIED
CONSTRAINT_IDENTIFIED
ZONE_CANDIDATE
ZONE_TRADABLE
ENTRY_REFINEMENT_REQUIRED
ENTRY_ALLOWED
WATCHLIST
VETO
```

## Machine-Readable Summary

```text
context_power is not enough

model = {
  position_state,
  constraint_set,
  constraint_exploitability,
  context_power,
  zone_promotion,
  destination_optionality,
  parent_map,
  child_execution_refinement
}

fixed anatomy = NDS rules
learned policy = which constraint/state gives lower cost and larger reward
```

## Short Formal Statement

Context power in NDS is not merely a strength score. The system must first identify structural position across Hook/Rally, bullish/bearish interpretations, and fractal parent-child scales. Then it must identify which NDS constraints exist in that position and whether those constraints are exploitable with low risk and high reward. X closure usually provides reversal power, Y closure improves zone precision and momentary energy, multiple closed sequences increase power, and symmetry confluence can promote a region into a trade zone or an entry Extreme. Higher timeframe remains dominant, while lower timeframe refines how the higher timeframe map is executed. Final output must include position, constraint strength, exploitability, zone promotion, optionality, and entry permission—not just raw context power.
