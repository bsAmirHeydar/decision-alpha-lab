# BASE-02 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
core ontology principle
scenario data model requirement
AI scenario-ranking requirement
execution-readiness requirement
```

It defines what a scenario must contain before it can become a dataset row or an execution intent.

## Proposed Scenario Object

```text
scenario_id
snapshot_id
direction
context_type
hook_reason_count
rally_reason_count
reason_vector
parent_context_state
current_context_state
child_context_state
fractal_support_state
approx_entry_zone_id
approx_entry_zone_quality
exact_entry_price
stop_price
destination_price
invalidation_id
invalidation_state
scenario_status
scenario_quality_score
execution_readiness_state
```

## Proposed Scenario Status States

```text
DIRECTIONAL_CASE_ONLY
ZONE_CANDIDATE
ENTRY_CANDIDATE
EXECUTION_READY
WEAK_ALIVE
INVALIDATED_DEAD
SUPERSEDED
AMBIGUOUS
```

## Proposed Dataset

```text
scenario_ledger_v1.csv
```

A future specialized dataset could store every alive or candidate scenario per market snapshot.

## Proposed Labels

```text
scenario_became_execution_ready
scenario_invalidated_before_entry
scenario_reached_entry_zone
scenario_exact_entry_filled
scenario_destination_before_invalidation
scenario_invalidation_before_destination
scenario_weakened_but_survived
scenario_died_by_parent_override
scenario_died_by_hook_rally_reclassification
```

## Proposed AI Modules

```text
Scenario Builder
Scenario Ranker
Scenario Status Classifier
Scenario Invalidation Model
Fractal Scenario Context Model
Execution Readiness Gate
```

## Open Questions

1. What is the minimum required reason count for a scenario to be considered alive?
2. Can a scenario be alive with only parent-scale support and no current-scale entry zone?
3. Can a scenario be execution-ready if the opposite scenario is still alive?
4. What exactly upgrades a directional case into a zone candidate?
5. What exactly upgrades a zone candidate into an entry candidate?
6. What exactly upgrades an entry candidate into execution-ready?
7. What makes a weak scenario worth keeping on watch?
8. What makes a weak scenario dangerous enough to block?
9. Can one scenario have multiple approximate entry zones?
10. Can one scenario have multiple exact entry candidates?
11. Can one directional scenario split into Hook-based and Rally-based sub-scenarios?
12. Should scenario invalidation be tracked separately from broker stop?
13. Should scenario death automatically cancel pending orders?
14. Should scenario weakening reduce rank score but keep watch mode?
15. Should parent-scale override mark a scenario dead or only downgrade it?

## Architecture Consequence

The future system should not only export final decisions.

It should export the scenario construction process.

This means the AI pipeline needs records before execution:

```text
directional case
zone candidate
entry candidate
execution-ready scenario
```

This allows models to learn not only whether trades worked, but how scenarios matured or died.
