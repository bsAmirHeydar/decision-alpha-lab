# SCN-R03 — Normalized Interpretation

## Core Claim

Scenario ranking in NDS is not a truth-selection problem.

The system should not force one scenario to become dominant unless the structure itself requires it.

The correct model is:

```text
Convex Opportunity Set
```

Multiple scenarios can remain alive at the same time if each has its own NDS evidence and offers a convex opportunity.

The goal is not to predict which scenario is correct.

The goal is to find which scenario offers:

```text
lower cost
larger profit
wider reward path
more open optionality
better convexity
```

## Scenario Does Not Need to Dominate

A scenario does not need to become the only dominant scenario.

Instead:

```text
each scenario is evaluated by its own evidence
each scenario can create its own convex trade
multiple scenarios can coexist
```

A bullish scenario and bearish scenario may both remain alive as conditional plans if both have valid NDS constraints and both offer favorable convexity at their own zones.

## Potential Over Correctness

The user explicitly states:

```text
Potential matters, not correctness.
```

This changes the ranking objective.

The model should not rank scenarios by "which one is most likely true" first.

It should rank by:

```text
which one is cheapest to be wrong on
which one pays most if right
which one has the most open reward path
which one has the best convex payoff shape
```

Correctness is secondary.

Payoff shape is primary.

## Convex Trade Definition

A convex trade in this context means:

```text
small controlled cost
large possible reward
open or wide profit path
favorable asymmetry
```

Suggested scoring components:

```text
entry_cost
stop_distance
distance_to_destination
reward_path_openness
optionality
explosion_potential
constraint_strength
```

A scenario may be low probability but still valuable if its cost is very low and its payoff is very open.

## Scenario Threads

The user says:

```text
we use each one of these threads
```

This means each scenario/zone family can be treated as a separate opportunity thread.

Suggested object:

```text
ScenarioThread
```

Each ScenarioThread should contain:

```text
scenario_id
zone_id
direction
evidence_set
constraint_set
entry_family
destination_set
cost_profile
reward_profile
convexity_score
state
```

## Ranking Objective

The ranking objective should be:

```text
maximize convexity before win rate
```

Rank scenarios by:

```text
cost-to-potential ratio
reward openness
optionality
zone quality
entry refinability
destination availability
constraint exploitability
```

Not by raw prediction confidence alone.

## Win Rate Comes After Convexity

The user gives a hard priority rule:

```text
after convexity, win rate matters, not before it
```

This means the system should first filter/rank by convexity.

Then, among convex candidates, win rate can be used to improve selection.

Order:

```text
1. Is the opportunity convex?
2. Is the cost small enough?
3. Is the reward path open enough?
4. Is the structural evidence acceptable?
5. After that, what is the win rate?
```

Win rate should not eliminate a high-convexity setup too early unless its tested performance shows that the convexity does not survive.

## Continuous Testing

Every scenario should be continuously tested.

This supports a research loop:

```text
scenario family
zone family
entry family
convexity profile
outcome distribution
post-convexity win rate
```

The model should keep a record of each scenario family, even if it is not currently primary.

## Multi-Zone Selection

If several zones are valid, the system does not need to choose only one.

It can keep several zones as conditional convex opportunities.

Suggested states:

```text
PRIMARY_CONVEX_OPPORTUNITY
SECONDARY_CONVEX_OPPORTUNITY
WATCHLIST_CONVEX_OPPORTUNITY
CONDITIONAL_LONG_PLAN
CONDITIONAL_SHORT_PLAN
VETOED_NON_CONVEX
```

The word "primary" should not mean "most true."

It should mean:

```text
best current cost-to-potential opportunity
```

## Veto Logic

A scenario or zone should be vetoed not because another scenario exists, but because it fails its own opportunity test.

Possible veto reasons:

```text
cost too high
reward too closed
destination too near
optionality too low
no exploitable constraint
zone not real
entry cannot be refined
stop is too wide
structure invalidated
parent context makes payoff poor
tested convexity does not survive
```

## Risk Allocation

Risk should be allocated according to convexity and tested usefulness, not merely probability.

Possible risk drivers:

```text
convexity_score
cost_profile
reward_openness
zone_quality
entry_refinement_quality
tested post-convexity win rate
scenario family stability
```

A scenario with a very small stop and very open reward can justify a position even if it is not the most likely scenario.

## Conditional Coexistence

Opposite directional scenarios can coexist as conditional plans.

Example:

```text
conditional long plan at one zone
conditional short plan at another zone
```

They are not both executed blindly.

They remain conditional until price reaches the relevant zone and lower-timeframe entry refinement appears.

## Ranking Updates

Scenario rank should update as the market changes.

Update triggers:

```text
price approaches zone
zone destroyed
destination reached
new sequence closes
X/Y closure changes
symmetry confluence changes
L view changes
entry cost changes
reward path opens or closes
```

Ranking is dynamic.

## Output Model

The final algorithmic output should be a list of live opportunity threads, not one forced answer.

Suggested output:

```text
ConvexOpportunitySet
```

Each item should contain:

```text
scenario_id
zone_id
direction
state
convexity_score
cost_score
reward_openness_score
optionality_score
post_convexity_win_rate
risk_budget
entry_permission_state
veto_reason
```

## Machine-Readable Summary

```text
scenario ranking is not truth ranking

goal = convex opportunities
potential > correctness
convexity before win rate

multiple scenarios can remain alive
multiple zones can remain alive
opposite plans can coexist conditionally

primary = best cost-to-potential opportunity
not necessarily most correct prediction
```

## Short Formal Statement

In NDS, multiple scenarios do not need to collapse into one dominant truth. Each scenario is evaluated by its own NDS evidence and by whether it offers a convex trade: lower cost, larger possible reward, wider reward path, and more open optionality. Potential matters more than correctness. Every scenario should be continuously tested, but ranking should first prioritize convexity and cost-to-potential quality. Win rate matters only after convexity has been established. The system should output a live Convex Opportunity Set containing primary, secondary, watchlist, conditional, and vetoed scenario threads.
