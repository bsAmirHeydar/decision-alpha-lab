# EXT-03 — Normalized Interpretation

## Core Claim

L2 is the minimum valid node level for Extreme because L1 is not structurally meaningful.

L2 gives the system the smallest valid anchor that still has a minimum amount of left/right confirmation.

This allows the system to detect more Extreme opportunities and preserve very small stop geometry.

However, L2 is a default, not a dogma.

Node level should remain testable and context-sensitive.

## L-Level Definition

The user's current definition:

```text
L2 = a node price where at least 2 candles on the left
     and at least 2 candles on the right do not reach that price.
```

This means L-level expresses local isolation of a price node.

The higher the L value, the more structurally isolated or broader the node may be.

## Why L1 Is Not Valid

L1 is considered meaningless.

Reason:

```text
L1 does not provide enough structural isolation.
L1 is too small to count as a valid node in this NDS logic.
L1 would create too many weak or noisy micro-nodes.
```

Therefore:

```text
L1 should not be used as the default Extreme anchor.
```

Suggested hard rule:

```text
L1_EXTREME_ANCHOR = rejected by default
```

unless a future manual NDS revision explicitly redefines it.

## Why L2 Is Default

L2 is the lowest meaningful node level.

This gives two important properties:

### 1. More Extreme opportunities

Using L2 allows the system to see more possible Extremes.

This is important because the project wants to test and exploit many narrow-risk Extreme entries.

### 2. Smaller stops

Using lower-level valid nodes keeps the entry and stop geometry small.

This preserves convexity.

The target idea:

```text
smaller stop
larger relative reward
more explosive R potential
```

This connects EXT-03 to EXT-01:

```text
Extreme is valuable because it can create narrow risk and convex reward.
```

## Why L3 or Higher May Be Useful

The user does not reject levels above L2.

Instead, higher L values may become useful when the cycle is larger.

Possible interpretation:

```text
larger cycle
larger structural context
larger anchor requirement
higher L may be more robust
```

But the tradeoff is:

```text
higher L may reduce number of opportunities
higher L may make stops wider
higher L may make entry later or deeper
higher L may reduce convexity
```

Therefore, higher L should be tested, not assumed.

## No Dogmatic Attachment to L2

The answer explicitly says:

```text
there is no dogmatic attachment to 2.
```

This means L2 is the default operational starting point, but the system should preserve flexibility.

Suggested formal state:

```text
anchor_level_default = L2
anchor_level_policy = flexible
anchor_level_test_required = true
```

## Structural Tradeoff

The node-level policy has a core tradeoff:

```text
lower valid L → more opportunities, smaller stops, more convexity, more fragility risk
higher L → fewer opportunities, potentially more robustness, wider stops, less convexity
```

This should become a testable research axis.

## Dataset Consequence

Future Extreme datasets should not only store that the anchor is L2.

They should also store possible alternate levels and compare them.

Required fields:

```text
anchor_node_level
candidate_node_levels_available
selected_anchor_level
anchor_level_reason
anchor_level_default_used
anchor_level_overridden
cycle_size_context
stop_distance_by_level
opportunity_count_by_level
```

## Testing Requirement

The project should explicitly test:

```text
L2 anchors
L3 anchors
L4 anchors
possibly adaptive L based on cycle size
```

L1 should be excluded unless manually redefined.

Recommended tests:

```text
L2 vs L3 vs L4
cycle-size conditioned L selection
stop-size comparison
reward distribution comparison
stop-hit-then-reverse comparison
limit-missed comparison
convexity comparison
```

## AI Relevance

AI should not redefine what L means.

But AI can learn how to select or rank valid L-level anchors after NDS has generated them.

Allowed learnable tasks:

```text
choose L2 vs L3 based on cycle size
rank candidate anchor nodes
estimate fragility of low-L anchor
estimate convexity of low-L anchor
recommend wider or narrower Extreme width
```

Forbidden task:

```text
AI invents a non-NDS node level or imports external pivot logic.
```

## Short Formal Statement

L2 is the default Extreme anchor because it is the minimum meaningful NDS node level. L1 is rejected as structurally meaningless. L2 preserves more opportunities and smaller stops, which supports convex Extreme entries. Higher L levels may be better in larger cycles, but this must be tested through an adaptive and context-sensitive node-level policy rather than treated as a fixed rule.
