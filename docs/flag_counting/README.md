# Flag Counting Documentation

## Active source of truth

Start here:

```text
docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
```

That file is the final decision source for Phoenix. If any older Flag Counting document conflicts with it, the current canon wins.

## Active implementation

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
mql5/Include/FlagCountingPhoenix/
```

Phoenix is the only active implementation path.

## Active canonical documents

Read in this order:

1. `FLAG_COUNTING_CURRENT_CANON.md` — final decisions and conflict resolver.
2. `FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md` — semantic F1/F2/F3 and Hook/ND contract.
3. `FLAG_COUNTING_ENGINEERING_PACK_V5.md` — engineering package index.
4. `engineering_pack_v5/` — definitions, explanations, algorithms, visualization contracts.
5. `implementation_ladder_v1/` — implementation order, interfaces, freeze gates, validation, audit/export.
6. `phoenix_rebuild/` — Phoenix-specific repair notes, subordinate to the current canon.

## Legacy/history documents

The following files remain useful as historical context, but must not be used as the decision source for new Phoenix code:

```text
FLAG_COUNTING_CONCEPT_SPEC_V2.md
FLAG_COUNTING_CONCEPT_SPEC_V3.md
FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md
FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md
FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md
FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md
FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md
FLAG_COUNTING_STATE_MACHINE_V2.md
FLAG_COUNTING_STATE_MACHINE_V3.md
FLAG_COUNTING_STATE_MACHINE_V4.md
FLAG_COUNTING_VNEXT_IMPLEMENTATION.md
FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md
```

M0007, VNext, and V6 are archived/reference implementations only.

## Non-negotiable rule

Flag Counting is a high/low-only, L-node-based, stateful sequence engine:

```text
ND/Hook -> F1 -> F2 -> F3 -> Extension/Lock
```

It is not a sliding-window pattern scanner, and the renderer is never allowed to invent or repair structure logic.

## Phoenix Level 11.5 raw audit export

Phoenix now includes a read-only raw audit export layer before renderer trust. Enable it from `FlagCountingPhoenixExperiment.mq5` with:

```text
InpExportAuditFiles = true
```

Default output goes to:

```text
MQL5/Files/FlagCountingPhoenix/latest_events.csv
MQL5/Files/FlagCountingPhoenix/latest_hooks.csv
MQL5/Files/FlagCountingPhoenix/latest_summary.csv
MQL5/Files/FlagCountingPhoenix/latest_manifest.csv
```

This export serializes the Level 11 canonical stream. It does not create, hide, repair, or draw structures.
