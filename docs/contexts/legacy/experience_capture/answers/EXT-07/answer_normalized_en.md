# EXT-07 — Normalized Interpretation

## Core Claim

When several L2 nodes are close to each other, the system should not necessarily collapse them into one single "true" anchor.

Each valid L2 node can be treated as a separate entry opportunity.

The logic is not:

```text
find the one node that predicts the market
```

The logic is:

```text
identify all structurally valid convex opportunities
rank or route them by reward potential, risk geometry, and expectancy
```

## No Single-Anchor Prediction Mindset

The answer rejects the idea that the system must always find one exact market formula.

This is important.

The system should not treat anchor selection as a classical prediction problem.

It should treat nearby L2 nodes as an opportunity set.

Suggested term:

```text
Extreme Anchor Opportunity Set
```

This means multiple anchors may remain alive at the same time if they are structurally valid.

## Each Nearby L2 Node Can Be an Opportunity

If several nearby L2 nodes exist, each can potentially define:

```text
its own near-death zone
its own entry price
its own stop behind node
its own reward profile
its own fill probability
its own invalidation event
its own convexity score
```

Therefore, the system should log all candidates before selecting or routing one.

## Selection Is Not Based on Win Rate Alone

Win rate is explicitly rejected as the primary criterion.

The system should not choose the anchor only because it has the highest probability of being right.

Instead, the anchor decision must account for:

```text
positive expectancy
convex reward
explosion potential
risk thinness
reward-to-risk asymmetry
right-tail potential
```

A lower-win-rate anchor may still be better if its losses are small and its reward potential is explosive.

## Positive Expectancy as the Main Criterion

The strategy is based on positive expectancy.

That means the correct question is not:

```text
which node is most likely to win?
```

The correct question is:

```text
which node creates the best expected opportunity after considering risk, reward, convexity, fill behavior, and invalidation?
```

This makes anchor selection a portfolio-like decision over opportunity candidates.

## Convexity-Based Ranking

The system should rank candidate anchors by convexity.

Possible ranking dimensions:

```text
risk_distance
stop_thinness
destination_openness
right_tail_potential
spread_to_risk_ratio
fill_probability
limit_miss_risk
stop_hit_then_reverse_risk
parent_context_support
scenario_alignment
```

But the final selection should not be reduced to one mechanical factor such as nearest, deepest, newest, or oldest.

## Multiple Anchors May Remain Alive

Because each valid L2 node can be an opportunity, the system should support:

```text
multiple_live_extreme_anchors
ranked_anchor_candidates
layered_entry_candidates
selected_anchor_for_order
secondary_anchor_watchlist
```

This allows the system to preserve optionality.

A selected anchor may be chosen for the current order, while other candidates remain alive as alternatives.

## Relationship to Parent Context

Parent confirmation can be a ranking feature, but not necessarily the only rule.

A parent-supported node may receive higher score.

However, another node may still be interesting if it offers better convexity, cleaner stop geometry, or more explosive destination.

Therefore, parent confirmation should be part of the reason vector and ranking logic, not necessarily a single hard override in every case.

## Relationship to Stop and Destination

A node with a better stop or more open destination may be preferable because the strategy cares about reward potential and expectancy.

Important candidate fields:

```text
stop_distance_raw
spread_to_stop_ratio
destination_distance
destination_openness
reward_to_risk_ratio
convexity_score
```

These are central to choosing between nearby L2 nodes.

## AI Relevance

AI should not be trained to answer only:

```text
which anchor is correct?
```

AI should be trained to:

```text
build an anchor opportunity set
score each candidate
rank candidates by expectancy and convexity
select current execution anchor if required
keep alternatives alive when valid
```

Possible AI outputs:

```text
candidate_anchor_rank
selected_execution_anchor
secondary_anchor_candidates
skip_all_candidates
layered_entry_allowed
```

## Execution Consequence

If the execution layer can only place one order, it should use the top-ranked anchor.

If the execution framework supports layered entries, it can allocate across multiple candidate anchors only after rules or tests prove that layered execution improves expectancy.

Until then, the safest architecture is:

```text
log all valid nearby L2 anchors
rank them
select one execution anchor
keep the others as watchlist candidates
```

## Short Formal Statement

When multiple valid L2 nodes are close to each other, each node is a potential Extreme entry opportunity. The system should not force a predictive single-anchor worldview. It should build an opportunity set, rank candidates by convexity, reward potential, risk geometry, destination openness, parent/context support, and expected value, and only then select an execution anchor if the execution layer requires one.
