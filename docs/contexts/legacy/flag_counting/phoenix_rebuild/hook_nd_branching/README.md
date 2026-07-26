# Hook / ND Branch-Sequence Documentation Pack

This package defines the Hook / ND component used by the Flag Counting Phoenix engine.
It is intentionally separated from the F1/F2/F3 sequence documents because Hook / ND is not a simple label or a single visual marker. It is a structural container that can hold multiple internal branch sequences.

The purpose of this package is to remove ambiguity before implementation. The engine must not treat every three or four raw nodes as ND. A Hook / ND exists only when the branch-sequence rules defined here are satisfied.

## Files

- `HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md`  
  Canonical conceptual and engineering contract for Hook / ND.

- `HOOK_ND_BRANCH_ALGORITHM_V1.md`  
  Step-by-step deterministic algorithm for extracting Hook / ND branches.

- `HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md`  
  Rendering contract for Hook / ND arcs, branch labels, ND text, and clean stacked chart labels.

- `HOOK_ND_IMPLEMENTATION_CHECKLIST_V1.md`  
  Engineering checklist for updating the Phoenix code safely.

## Core idea

A Hook is not one branch. A Hook can contain many branch sequences. The number of branch sequences is not capped. What is capped is the number of internal same-side nodes inside each branch sequence. After adaptive L normalization, every branch sequence must contain at most four counted internal nodes.

A Hook becomes ND only when at least one internal branch sequence contains exactly three or four counted nodes and satisfies the cycle retracement rule.

Two counted nodes are not ND.

Five or more counted nodes are not directly accepted. They trigger adaptive L escalation and a full rebuild of the Hook context.
