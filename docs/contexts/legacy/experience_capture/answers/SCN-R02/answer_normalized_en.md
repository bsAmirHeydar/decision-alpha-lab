# SCN-R02 — Normalized Interpretation

## Core Claim

A Potential Zone in NDS is not just a level.

It is a price range where multiple NDS constraints and fractal readings combine to create a high-potential explosion point.

Formal definition:

```text
Potential Zone = price range where the current structural position becomes exploitable with lower cost and larger reward potential
```

The zone is the bridge between context and entry.

```text
Context = what is the situation?
Zone = where is this situation exploitable?
Entry = what is the exact lower-scale anchor with smallest practical stop?
```

## Zone as a Price Range

A zone is explicitly a price range.

It is not a single price and not merely a node.

Recommended object:

```text
PotentialZone
```

Core fields:

```text
zone_low
zone_high
zone_start_price
zone_end_price
zone_mid_price
zone_direction
zone_source_constraints
zone_parent_context
zone_child_refinement_state
```

## Zone as Explosive Area

A valid zone should represent:

```text
high-potential reversal area
lower cost
larger explosion
favorable optionality
```

Therefore, zone quality is not just reversal probability.

It must include:

```text
risk compression
reward expansion
destination openness
constraint strength
entry refinability
```

## Context vs Zone

The user gives a precise distinction:

```text
Context tells the situation.
Zone tells where that situation is exploitable.
```

So context alone is not enough for tradeability.

A context becomes a zone only when the system identifies a price range where the constraints of that context can be exploited.

This supports the hierarchy:

```text
Context → Position → Constraint → Zone → Entry
```

## Zone Sources

The user says many combinations can create zones.

A zone can be built from any exploitable NDS constraint.

Possible zone sources:

```text
Hook completion
CycleHook near-death
F-counting relation
F2 >= F1 constraint
F3 completion or trend-start relation
X closure
Y closure
multi-sequence closure
symmetry confluence
origin node area
Hook start boundary
destination structure
parent-child fractal contradiction/completion
```

No single source should monopolize zone creation.

The system should store zone source constraints as a set.

## Example 1 — Higher Bearish F2 and Middle Bullish F3

Example:

```text
higher timeframe = bearish F2
middle timeframe = bullish F3
```

Then the system asks:

```text
which Hook is this F3 completing?
```

If that Hook is near death, then the range between the near-death area and the origin node price of that Hook can become the zone.

General form:

```text
PotentialZone = [CycleHook ND area, CycleHook origin node price]
```

This is a fractal zone because it combines:

```text
higher timeframe F-state
middle timeframe F-state
Hook completion
CycleHook near-death
origin boundary
```

## Example 2 — F2 >= F1 and CycleHook Near-Death

Rule:

```text
F2 is greater than or equal to F1
```

If price has already moved by the size of F1 and is also near the death area of a CycleHook, this can create a zone.

The trade can be framed as betting until:

```text
the waist / midpoint of F2 is eaten
```

This creates a zone from a combination of:

```text
F-counting constraint
minimum movement completion
CycleHook ND
destination to F2 waist/midpoint
```

## Zone From Any Constraint

The user states:

```text
we can use any constraint and create a zone
```

This is important.

NDS should not have only one zone recipe.

Instead, it should support:

```text
zone_recipe_id
zone_constraint_set
zone_source_model
zone_training_family
```

Different zone families should be testable.

## Zone and Lower-Timeframe Entry

After a zone is identified, exact entry is refined on a lower timeframe.

Inside the zone, the system should search for:

```text
entry-level Extreme
lower-timeframe Hook closure
smallest practical stop
limit reversal setup
```

Important terminology:

There are two different uses of the word Extreme.

### Hook Extreme

The opposite Extreme inside a CycleHook/Hook structure.

### Entry-Level Extreme

The precise lower-timeframe entry anchor where the lower-timeframe Hook closes as much as possible and allows the smallest practical stop.

This answer refers to entry-level Extreme when discussing exact entry inside a zone.

## Zone and Symmetry

Symmetry usually helps define the start of the zone.

Possible rule:

```text
symmetry confluence → zone_start_price
```

The end of the zone can be behind the Hook start.

Possible rule:

```text
Hook start / origin boundary → zone_end_price
```

Thus a zone may be bounded by:

```text
start = symmetry projection / confluence
end = behind Hook start / origin boundary
```

This should remain learnable, because different zone families may use different boundary logic.

## Zone Invalidation

The user says:

```text
A zone becomes invalid when the area itself is destroyed.
```

This should be interpreted structurally.

A zone is destroyed when the constraints that created it no longer exist or are no longer exploitable.

Possible invalidation causes:

```text
origin boundary crossed
CycleHook death
zone source constraint invalidated
parent context changes
destination already reached
price passes beyond the zone in a way that destroys low-cost reversal logic
entry-level structure fails
optionality collapses
```

The exact rules are zone-family dependent and should be trained/tested.

## Training Granularity

This answer introduces a major training architecture.

Training should proceed in layers.

### Layer 1 — Global Training

Train across:

```text
all markets
all conditions
```

Goal:

```text
discover general NDS zone rules
```

### Layer 2 — Market-Specific Training

Train separately for each market.

Example:

```text
gold-specific behavior
indices-specific behavior
FX-specific behavior
```

Goal:

```text
capture market personality
```

### Layer 3 — Market-Timeframe Training

Train separately for each timeframe inside each market.

Example:

```text
XAUUSD H1
XAUUSD M15
EURUSD H1
```

Goal:

```text
capture scale-specific zone behavior
```

### Layer 4 — Dynamic Weight Trend

Even inside one market-timeframe, behavior may not be stable.

The model may need to learn changing weights over time.

Example:

```text
In XAUUSD H1, Hook weight may gradually decrease while F3-as-trend-start weight increases.
```

This is a dynamic weighting problem.

Suggested object:

```text
ZoneWeightRegime
```

This means the system should not assume one permanent weight model.

## Zone Output

The final zone output should be:

```text
a price range that indicates a good high-potential reversal
```

With target qualities:

```text
lower cost
larger explosion
better optionality
entry refinability
```

Recommended output classes:

```text
ZONE_CANDIDATE
POTENTIAL_ZONE
TRADABLE_ZONE
ENTRY_REFINEMENT_REQUIRED
EXTREME_ALLOWED_INSIDE_ZONE
ZONE_INVALIDATED
ZONE_EXPIRED
ZONE_DESTROYED
```

## Machine-Readable Summary

```text
Zone = exploitable price range
Context = situation
Zone = situation exploitable here
Entry = lower-timeframe Extreme inside zone

Zone source = any NDS constraint or combination
Zone quality = low cost + high explosion + optionality
Zone start often = symmetry confluence
Zone end may be behind Hook start / origin
Zone invalidation = area/constraint destroyed

Training layers:
global
market-specific
market-timeframe-specific
dynamic weight trend
```

## Short Formal Statement

A Potential Zone in NDS is a price range where multi-sided and fractal analysis shows that the current structural position is exploitable with lower cost and larger explosion potential. Context tells the situation; zone tells where that situation can be used. A zone may be created from many combinations of NDS constraints, including Hook completion, CycleHook near-death, F-counting relations such as F2 >= F1, X/Y closure, symmetry confluence, origin boundaries, and destination structure. Once a zone exists, exact entry is refined on a lower timeframe through an entry-level Extreme, where a lower-scale Hook closes as much as possible and allows the smallest practical stop. Zone logic must be trained in layers: global, market-specific, market-timeframe-specific, and dynamic weight-regime level.
