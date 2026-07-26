# Hook Sequence Partition Fix Patch

## Purpose

This patch corrects Hook Phase 02 sequence construction.

It replaces overlapping end-backward branch enumeration with a canonical greedy old-to-new partition:

- positive Hook sequences consume valleys;
- negative Hook sequences consume peaks;
- the first unused node becomes node `1` of the next sequence;
- the sequence is extended to the end of the raw list;
- only stricter continuation nodes are accepted;
- consumed nodes cannot seed or participate in overlapping later sequences.

## Why

The prior engine could stop a sequence at `2` even when valid `3`/`4` continuation nodes existed, then allow already-used nodes to become `1` of another displayed branch. This created excessive labels and made the Hook view look structurally wrong.

## Code changed

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh
```

## Documentation added

```text
docs/nds_hook_architecture/46_phase34_hook_sequence_greedy_partition_ownership.md
docs/obsidian_hook/01_concepts/Greedy_Hook_Sequence_Partition.md
docs/obsidian_hook/02_policies/Consumed_Node_Cannot_Start_New_Hook_Sequence.md
docs/obsidian_hook/03_architecture/Phase_34_Hook_Sequence_Partition_Guard.md
docs/obsidian_hook/04_debug/Hook_Sequence_Numbering_Debug_Checklist.md
```

## Scope

This patch changes Hook Phase 02 sequence ownership and numbering only.

It does not change:

- F-counting logic;
- Rally logic;
- Zone logic;
- execution logic;
- broker behavior;
- risk sizing;
- order sending.
