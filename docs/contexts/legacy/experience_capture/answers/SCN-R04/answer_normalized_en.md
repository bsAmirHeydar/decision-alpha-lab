# SCN-R04 — Normalized Interpretation

## Core Claim

A scenario in NDS is born from a set of respected constraints.

It remains alive, updates, reprices, loses rank, gains rank, or dies based on two main dimensions:

```text
1. constraint integrity
2. relative weight versus other scenarios
```

The system does not need to decide scenario life/death by prediction correctness.

It should track:

```text
how much of the scenario's own constraint set remains untouched
how its weight changes compared with new scenarios and updated existing scenarios
```

## Scenario as Constraint-Based Object

A scenario is not a loose idea.

It is an object created by a specific set of NDS constraints.

Suggested object:

```text
ScenarioThread
```

Each ScenarioThread should keep:

```text
scenario_id
constraint_set
zone_set
destination_set
entry_family
convexity_profile
weight
state
```

The source constraints are part of the scenario identity.

## Constraint Integrity

The most important update signal is:

```text
how much of the scenario's constraints remain untouched
```

Suggested metric:

```text
constraint_integrity_score
```

This score should reflect whether the original reasons for the scenario are still structurally valid.

Examples of constraints that may need integrity tracking:

```text
Hook constraints
CycleHook constraints
Rally constraints
X closure
Y closure
multi-sequence closure
symmetry confluence
ND boundary
origin boundary
destination logic
open one-and-two logic
parent context
zone boundary
entry-level refinement condition
```

## Untouched Constraint Rule

The phrase "untouched constraints" should not mean only price not touching a level.

It means:

```text
the structural limitation/reason that created the scenario has not been violated or destroyed
```

A constraint can be untouched, partially weakened, consumed, invalidated, or replaced.

Suggested states:

```text
CONSTRAINT_INTACT
CONSTRAINT_WEAKENED
CONSTRAINT_CONSUMED
CONSTRAINT_REPLACED
CONSTRAINT_INVALIDATED
```

## Relative Weight

A scenario is also evaluated against other scenarios.

The system should compare a scenario with:

```text
newly created scenarios
previous scenarios that have been updated
opposite-direction scenarios
same-direction alternative zones
```

A scenario's rank changes when its relative weight changes.

Suggested metric:

```text
relative_scenario_weight
```

This weight should be updated dynamically.

## Scenario Update

A scenario updates when:

```text
its constraint set remains largely intact
but new market information changes its weight, zone, cost, destination, or optionality
```

Update does not mean death.

Update means the scenario remains a valid thread but its current usefulness changes.

## Scenario Repricing

A scenario should be repriced when its identity remains valid but its tradeable expression changes.

Repricing may update:

```text
zone boundaries
entry price
stop position
destination path
risk budget
convexity score
optionality score
```

Repricing is valid when:

```text
the core constraint set is still intact
but new nodes, new sequence state, new L view, new symmetry, or new zone information changes the cost/reward profile
```

## Scenario Death

A scenario dies when its core constraint set is no longer intact.

Death should be based on constraint failure, not merely lower rank.

Suggested death reasons:

```text
core constraint invalidated
origin boundary crossed
CycleHook dead
zone destroyed
required destination already consumed in a way that removes payoff
parent context invalidates the structural premise
convexity disappears because the original constraint no longer exists
```

A scenario can lose rank without dying.

## Veto vs Death

Death means the scenario's structural reason no longer exists.

Veto means the scenario may still structurally exist, but it should not be traded.

Suggested distinction:

```text
DEAD = scenario constraint identity broken
VETOED = scenario exists but is not worth trading
```

Veto reasons may include:

```text
cost too high
reward too closed
optionality too low
entry cannot be refined
too many better scenarios exist
risk budget exhausted
tested performance poor
```

## Watchlist

A scenario should move to watchlist when:

```text
constraints are still alive
but current tradeability is not sufficient
```

Examples:

```text
zone not reached yet
entry refinement not available
relative weight too low
better scenarios exist
cost/reward not good enough now
waiting for lower-timeframe confirmation inside zone
```

Watchlist is not death.

## Rank and Weight Update

Scenario rank should update whenever:

```text
new scenario appears
existing scenario updates
constraint integrity changes
zone boundary changes
destination opens or closes
entry cost changes
convexity changes
optionality changes
parent/child context changes
```

The rank update engine should compare all live ScenarioThreads in the current ConvexOpportunitySet.

## Scenario State Model

Suggested scenario states:

```text
SCENARIO_BORN
SCENARIO_ALIVE
SCENARIO_UPDATED
SCENARIO_REPRICED
SCENARIO_WEIGHT_INCREASED
SCENARIO_WEIGHT_DECREASED
SCENARIO_PRIMARY
SCENARIO_SECONDARY
SCENARIO_WATCHLIST
SCENARIO_TRADABLE
SCENARIO_ENTRY_PENDING
SCENARIO_VETOED
SCENARIO_DEAD
SCENARIO_ARCHIVED
```

## Constraint-Based Weighting

A scenario's weight should depend on:

```text
constraint_integrity_score
constraint_strength
convexity_score
cost_to_potential_ratio
reward_path_openness
optionality_score
relative_rank_against_other_scenarios
post_convexity_performance
```

This links SCN-R04 back to SCN-R03:

```text
potential over correctness
convexity before win rate
```

## Machine-Readable Summary

```text
Scenario = constraint-born opportunity thread

scenario update depends on:
- own constraint integrity
- relative weight versus other scenarios

alive = core constraints still intact
repriced = core constraints intact but expression changes
watchlist = alive but not currently tradeable
vetoed = alive but not worth trading
dead = core constraint identity broken
```

## Short Formal Statement

A scenario in NDS is created because a set of structural constraints has been respected. Its update, repricing, ranking, veto, or death should be determined by how much of those constraints remain untouched and how its relative weight changes compared with new scenarios or previously existing scenarios that have updated. A scenario can lose rank without dying. Repricing happens when the core constraint identity remains valid but the tradeable expression changes. Death happens when the core constraints that created the scenario are destroyed. Veto means the scenario still exists structurally but is not worth trading.
