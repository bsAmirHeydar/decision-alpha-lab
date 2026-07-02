# EXT-04 — Normalized Interpretation

## Core Claim

L2 should not be treated as a blind permanent rule.

The selected L coefficient must be tested.

Lower L values create more entries, but entry frequency alone is not enough.

The system must evaluate the tradeoff between:

```text
entry frequency
entry quality
win rate
reward size
convexity
fragility
```

## L Coefficient as a Policy Variable

The answer reframes the L level as a coefficient or parameter that belongs to the anchor-selection policy.

This means:

```text
L2 is a default candidate,
not an untouchable final rule.
```

Future systems should test multiple L values and compare their behavior.

Possible candidate levels:

```text
L2
L3
L4
adaptive L
```

## Lower L Creates More Entries

A lower L coefficient creates more Extreme opportunities.

Benefits:

```text
more entry candidates
more chances to capture very narrow-risk moves
more convex opportunities
more lower-timeframe refinement
```

Risks:

```text
more noise
more fragile stops
more missed fills
more stop-hit-then-reverse cases
lower win rate
higher execution sensitivity
```

## Higher L May Improve Quality

A higher L coefficient may reduce entry count but improve quality.

Possible benefits:

```text
more structurally isolated anchor nodes
less noise
more robust node selection
better win rate
cleaner entries
```

Possible costs:

```text
fewer entries
larger stops
lower convexity
later entry
reduced right-tail potential
```

## Reward vs Win Rate

The user explicitly states that sometimes reward outweighs win rate, and sometimes win rate outweighs reward.

This means L selection must not be judged only by win rate.

Evaluation must include both:

```text
hit rate / win rate
R distribution
right-tail payoff
left-tail loss
profit factor
expected R
drawdown behavior
path cleanliness
execution difficulty
```

A low-win-rate L2 strategy may still be valuable if its reward tail is large and losses remain small.

A higher-win-rate L3 strategy may be better if L2 is too fragile in a specific context.

## Context Validity

The answer does not fix L2 to Hook, Rally, buy, or sell.

Instead, it implies that L validity must be tested across contexts.

The future system should compare L-level behavior across:

```text
Hook context
Rally context
bullish scenarios
bearish scenarios
parent/current/child scale relationships
large cycles
small cycles
different entry families
```

This means L selection should be stored as a context-conditioned policy, not as a single global setting.

## Scale Role

The answer also supports the idea that lower-scale L selection is mainly an entry refinement tool.

The higher scale may define:

```text
direction
region
context power
scenario
```

The lower scale then selects the L-level anchor for precise entry.

So L2 on the lower scale may often be a trigger/refinement, while the higher scale remains the decision context.

## Testing Requirement

The correct next step is a structured L-level comparison.

Suggested tests:

```text
L2 vs L3 vs L4
L2 in Hook vs L2 in Rally
L2 in buy vs L2 in sell
L2 on lower scale with higher-scale direction
L2 under large-cycle vs small-cycle contexts
L2 reward-tail vs L2 win-rate
L3 reward-tail vs L3 win-rate
adaptive L policy vs fixed L2
```

## AI Relevance

AI can learn an L selection policy only after deterministic NDS node candidates are built.

The AI task should not be:

```text
invent nodes
```

The AI task should be:

```text
select or rank valid NDS node levels based on context
```

Possible AI outputs:

```text
use_L2
use_L3
use_higher_L
use_layered_L2_L3
skip_extreme_anchor
```

## Short Formal Statement

L2 is a default candidate, not a blind law. Lower L creates more entries and preserves convexity, but may reduce quality. Higher L may improve quality and win rate, but can reduce frequency and reward. The correct L coefficient must be tested by context and evaluated through both win rate and reward distribution, not by one metric alone.
