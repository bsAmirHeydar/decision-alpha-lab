---
title: NDS Entry Data and Audit Schema
status: implemented_v1
version: 1.0.0
---
# NDS Entry Data and Audit Schema

## 1. Output chain

```text
nds_entry_structure_snapshot.csv
nds_entry_setup_candidate.csv
nds_entry_trade_plan.csv
nds_entry_command_preview.csv
nds_entry_pipeline_summary.csv
```

## 2. Traceability keys

Each layer stores the key of its source:

```text
Structure.structure_key
Zone.zone_key
Setup.source_structure_key
Setup.source_zone_key
TradePlan.source_setup_id
Command.source_plan_id
Pipeline.pipeline_key
```

This provides a causal chain from a valid Hook to a command preview.

## 3. Knowledge-time rules

Every source field must be available at the time the Setup is created. Future persistent versions must record both:

```text
event_time
knowledge_time
```

The current snapshot uses closed-bar Phoenix input and current generation time. It must not be interpreted as a historical event ledger yet.

## 4. Required future ledgers

```text
nds_setup_ledger.csv
nds_setup_transition_ledger.csv
nds_zone_lifecycle_ledger.csv
nds_trade_plan_revision_ledger.csv
nds_command_ledger.csv
nds_execution_reconciliation_ledger.csv
```

## 5. Dataset unit

The preferred research unit is:

```text
HookZoneSetupEvent
```

not a candle and not a generic Hook shape.

Suggested eventual fields include:

```text
Hook family
parent Hook/F3 lineage
Zone width
Zone freshness
entry and death edges
child refinement
activation/touch counts
MFE/MAE
potential/width
path smoothness
time to expansion
stop efficiency
tail participation
```
