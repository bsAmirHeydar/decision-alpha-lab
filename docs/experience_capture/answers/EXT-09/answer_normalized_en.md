# EXT-09 — Normalized Interpretation

## Core Claim

Extreme anchor-node quality is secondary.

The primary edge is not in the isolated quality of the Extreme itself.

The primary edge comes from:

```text
understanding context
finding the correct potential zone
being exposed to explosive reward opportunities
preserving positive expectancy
```

Extreme is an entry point, not the source of the thesis.

## Extreme Quality Is Not the First Layer

The answer explicitly states that the quality of the Extreme itself is not the main thing.

This means the architecture should not begin by asking:

```text
is this Extreme high quality in isolation?
```

It should begin by asking:

```text
is this the correct context?
is this a potential-rich zone?
is reward exposure large enough?
does the opportunity have positive expectancy?
```

Only after that should it evaluate the Extreme entry point.

## Correct Priority Order

The implied priority order is:

```text
1. Context
2. Potential zone
3. Reward / explosive exposure
4. Entry point / Extreme
5. Win rate improvement
```

This matches prior answers:

```text
Context first
Zone second
Entry third
Reward first
Win rate second
```

## Potential Over Win Rate

The strategy is not optimized primarily for win rate.

The main goal is to find places with strong potential and trade them with small risk.

This means a low-win-rate Extreme family can still be valid if it produces large reward relative to losses.

The key evaluation metric is:

```text
positive expectancy
```

not win rate alone.

## Anchor Quality May Still Be Learnable

The answer does not forbid studying anchor quality.

It says:

```text
train on these Extremes and see; maybe there is a rule.
```

Therefore, anchor quality should not be a hard-coded assumption at first.

It should become a learnable and testable policy layer.

Possible learnable anchor-quality factors:

```text
path cleanliness toward the node
prior touches
node age
parent-context support
destination openness
stop thinness
spread-to-stop ratio
limit-miss behavior
stop-hit-then-reverse behavior
post-entry expansion behavior
```

But these should enter only after testing.

## Human-in-the-Loop Training

The answer defines an important model-development workflow.

The AI should not silently learn and deploy.

The desired workflow is:

```text
AI trains
AI reports what it learned
human reviews the learned rule or pattern
human gives opinion
tests are run
the policy is accepted, rejected, or branched
```

This is a human-in-the-loop research loop.

## Layered and Branch-by-Branch Training

Training should not be a single monolithic model.

It should be layered and branch-based.

Suggested structure:

```text
branch by entry family
branch by context
branch by anchor-level policy
branch by reward-first objective
branch by win-rate-improvement objective
branch by algorithm type
```

This means the research system should preserve multiple experiment branches rather than collapse everything into one model.

## Multiple Algorithms

The user wants training with different algorithms.

This implies the future lab should support:

```text
rule-based baselines
tree-based models
ranking models
classification models
regression models
policy models
ablation tests
negative controls
branch comparison
```

The goal is not to find a magic formula.

The goal is to see which NDS-native patterns improve expectancy while preserving reward potential.

## AI Relevance

AI should be allowed to investigate anchor-node quality.

But it must stay inside the NDS boundary and must report learned patterns before they are accepted.

Allowed AI tasks:

```text
learn whether path cleanliness improves expectancy
learn whether prior touches matter
learn whether parent-zone proximity matters
learn whether some anchor nodes are too weak
learn whether anchor quality can improve win rate without reducing reward
```

Forbidden AI tasks:

```text
replace context and zone with isolated anchor quality
optimize win rate while destroying reward
use non-NDS concepts
silently deploy learned rules without review and testing
```

## Short Formal Statement

Anchor-node quality is not the primary edge. Extremes are entry points used after context and potential zone have already been established. The core criterion is positive expectancy through reward and explosive potential, not win rate alone. Anchor quality may still be trained and discovered, but learned patterns must be reported to the human, reviewed, tested, and developed in layered experiment branches with multiple algorithms.
