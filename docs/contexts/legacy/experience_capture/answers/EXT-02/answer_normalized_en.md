# EXT-02 — Normalized Interpretation

## Core Claim

Extreme does not generate the directional thesis.

Extreme does not generate the scenario.

Extreme is the lower-timeframe entry mechanism used after the higher-level NDS analysis has already defined:

```text
direction
region
scenario
context
```

The anchor node for Extreme belongs to NDS node logic, not RTV.

## RTV Is Excluded

RTV must not be used as a source for `extreme_anchor_node_id`.

RTV is explicitly outside NDS.

Therefore:

```text
RTV is not an allowed node source for Extreme.
RTV is not an allowed reason source.
RTV is not an allowed scenario source.
RTV should not be part of NDS datasets.
```

This reinforces BASE-04 and BASE-06:

```text
NDS-only ontology is a hard rule.
External research ideas do not enter the decision system unless explicitly converted into NDS.
```

## Extreme Is an Entry Mechanism, Not the Scenario Engine

The NDS process is layered.

### Layer 1 — Multi-layer NDS analysis

The system first analyzes the market using:

```text
Hook
Rally
F-counting
Node-counting
fractal context
multi-scenario logic
context power
```

### Layer 2 — Direction and region decision

The system then decides:

```text
which direction is relevant
which broad region is relevant for that direction
which scenario is alive or dominant
```

### Layer 3 — Lower-timeframe entry refinement

Only after direction and region are defined does the system move to a lower timeframe and search for an Extreme entry.

This means Extreme is not the whole strategy.

Extreme is an execution/refinement entry family.

## Anchor Node Source

The anchor node should come from NDS-native node logic.

The answer does not yet define one exact engine name, but it clearly excludes RTV and implies that the anchor node must be produced by NDS anatomy.

Possible NDS-native sources:

```text
Node-counting
Hook/Rally-derived node state
F-counting-derived structural context
X-axis node structure
```

The future system should treat `extreme_anchor_node_id` as an NDS node selected after scenario/region decision.

## L2 Default Logic

L2 was selected as the default because lower-level nodes allow more Extreme opportunities.

The key idea:

```text
large cycles can exist,
but entries can remain small by using lower-level nodes.
```

This allows the system to keep:

```text
high reward potential
narrow risk
entry precision
convex payoff
```

However, the user explicitly says this should be flexible.

Therefore, L2 should not become a rigid mechanical rule.

Suggested formal interpretation:

```text
L2 is the default anchor-node level for Extreme refinement,
but node-level selection should remain flexible and context-sensitive.
```

## Flexibility Requirement

The anchor-node selection must not be too rigid.

The system should not simply say:

```text
always use L2
```

Instead, it should support:

```text
default L2
context-dependent node level
lower-timeframe refinement
scenario-region-dependent anchor selection
```

This implies a future policy layer:

```text
Extreme Anchor Node Selection Policy
```

This policy can be rule-based first and learnable later.

## Relationship Between Direction, Region, and Extreme

The correct flow:

```text
NDS analysis
→ scenario direction
→ scenario region
→ lower-timeframe refinement
→ Extreme anchor node
→ entry
→ stop behind node
```

Incorrect flow:

```text
Extreme appears
→ infer direction from it directly
```

Extreme alone should not decide direction.

It should serve the direction/region already defined by higher-level NDS context.

## AI Relevance

AI should not train an Extreme model as if Extreme is a standalone predictor.

The Extreme model must receive upstream context:

```text
scenario direction
scenario region
context power
fractal state
entry family request
```

Then it can learn:

```text
which lower-timeframe anchor node is best
whether L2 is suitable
whether another node level is better
how tight the entry should be
whether the Extreme should be skipped
```

## Short Formal Statement

RTV is excluded from NDS and must not produce Extreme anchor nodes. Extreme is not a direction engine or scenario engine; it is a lower-timeframe entry-refinement mechanism used only after NDS anatomy has defined direction and region. L2 is the default anchor level because it keeps entries small even inside large cycles, but anchor selection must remain flexible and context-sensitive rather than rigidly mechanical.
