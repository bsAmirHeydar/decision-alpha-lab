# Phase 09 Ranking Dashboard Specification

## Mission

Phase 09 exists to transform the raw statistical tables from Phase 08 into a readable research-ranking surface. The layer answers questions such as:

- Which cycle groups have the strongest average R?
- Which direction behaves better inside each CG?
- Which hunter-clean role has better win rate?
- Which families are unstable because of stop streaks?
- Which combinations deserve later review by the strategy architect?

This is not an execution layer. Rankings are observations, not rules.

## Ranking Population

The ranking population is built from Phase 08 report rows, not from live signals directly. This means Phase 09 inherits the statistical boundary of Phase 07 and Phase 08:

1. Only confirmed tradeable outcomes entered Phase 07.
2. Phase 08 aggregated those outcomes into statistical buckets.
3. Phase 09 ranks those buckets.

## Report Families

Phase 09 can read:

| Report | Purpose |
|---|---|
| Overall | Whole strategy health |
| By CG | Each cycle group as a family |
| By Direction | BUY vs SELL behavior |
| By CG + Direction | Direction inside each CG |
| By Role | SPX hunter / NDX clean vs reverse |
| By CG + Direction + Role | Most granular current research family |

## Ranking Output

Each row receives:

- quality score
- grade
- shortlist eligibility
- warning flags
- recommendation text

The recommendation text is intentionally non-executional. It says `research_shortlist_candidate_not_execution_rule`, not `trade this`.

## Core Doctrine

Phase 09 must not mutate strategy. A strong-ranked bucket cannot automatically become a filter. A weak-ranked bucket cannot automatically be disabled. That promotion belongs to a later decision gate.
