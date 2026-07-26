# EXT-10 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
veto model principle
negative-example labeling rule
context-zone quality rule
entry-precision trap warning
```

## Main Design Consequence

The Veto Model should not be an isolated Extreme geometry filter.

It should combine:

```text
context validity
zone validity
scenario validity
reward exposure
entry geometry
```

## Proposed Hard Rules

```text
EXTREME_GEOMETRY_ALONE_IS_NOT_ENOUGH
CONTEXT_AND_ZONE_REQUIRED_BEFORE_ENTRY
VETO_CAN_BLOCK_PRECISE_ENTRY_IF_CONTEXT_ZONE_IS_WEAK
```

## Proposed Flexible Rules

```text
anchor quality may be learned
entry precision may improve execution
but neither can replace context and zone
```

## Proposed Datasets

```text
extreme_veto_dataset_v1.csv
extreme_negative_examples_v1.csv
context_zone_extreme_quality_v1.csv
deceptive_extreme_ledger_v1.csv
```

## Proposed Fields

```text
scenario_id
region_id
entry_family_type
extreme_id
anchor_node_id

extreme_geometry_present
context_valid
zone_valid
scenario_alive
parent_context_support
destination_open
reward_exposure_score
potential_zone_score
entry_precision_score

veto_required
veto_reason
deceptive_extreme_label
good_extreme_label
```

## Proposed Labels

```text
GOOD_EXTREME_CONTEXT_ZONE_VALID
DECEPTIVE_EXTREME_CONTEXT_INVALID
DECEPTIVE_EXTREME_ZONE_INVALID
DECEPTIVE_EXTREME_LOW_POTENTIAL
DECEPTIVE_EXTREME_NO_DESTINATION
DECEPTIVE_EXTREME_PARENT_CONFLICT
ENTRY_PRECISION_TRAP
VETO_EXTREME
ALLOW_EXTREME
```

## Proposed AI Modules

```text
Context-Zone Extreme Veto Model
Deceptive Extreme Classifier
Extreme Negative Example Builder
Entry Precision Trap Detector
Reward Exposure Gate
Potential Zone Quality Gate
```

## Open Questions

1. What exact minimum context conditions are required before an Extreme can be good?
2. What exact minimum zone conditions are required before an Extreme can be good?
3. Should parent-context conflict be a hard veto or a score penalty?
4. Can a high-convexity Extreme survive weak context?
5. Can a strong context save a low-quality Extreme entry?
6. Should the Veto Model output a score, class, or both?
7. Should deceptive Extremes be labeled after stop-out only, or at pre-entry time?
8. What is the difference between a bad Extreme and a good Extreme that simply loses?
9. Should a near-node entry with no open destination always be vetoed?
10. Should reward exposure have a minimum threshold?
11. Should the first Veto Model be rule-based before AI training?
12. Should every vetoed Extreme remain logged for later audit?
13. Should Veto be allowed to block an entry even if anchor geometry is excellent?
14. Should low win-rate but high-reward Extremes be protected from excessive vetoing?
15. How should we avoid a Veto Model that improves win rate by destroying reward?

## Attachment Index

No images were provided for this answer.
