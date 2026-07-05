# Phase 26 — Doc-Aligned Hook / ND Branch Rebuild

## Why

The earlier Phase 17–25 visual work treated each strict sequence as if it could be rendered as an independent Hook. That contradicted the Hook / ND documentation:

- Hook / ND is a structured phase container.
- Internal branch sequences are counted inside that container.
- Numbered branch nodes are same-side adverse nodes only.
- Low-side / positive Hook uses lows / valleys.
- High-side / negative Hook uses highs / peaks.
- Branches are built end-backward and then labelled old-to-new.
- Branches with more than four counted nodes are not valid readable output.
- Labels must be collected and stacked deterministically.
- The semantic chart view must not draw straight sequence wiring.

## Source documents used as authority

- `docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION.md`
- `docs/flag_counting/engineering_pack_v5/03_explanations/ND_HOOK_BRANCHING_EXPLAINED.md`
- `docs/flag_counting/engineering_pack_v5/04_algorithms/HOOK_BRANCH_ENGINE_ALGORITHM.md`
- `docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md`
- `docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1.md`
- `docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md`
- `docs/nds_hook_architecture/02_cyclehook_object_model.md`
- `docs/nds_hook_architecture/03_sequence_builder.md`
- `docs/nds_hook_architecture/05_visualization_and_diagnostics.md`

## Root fixes

### 1. Branch builder

`FP_HookPhase02Rules.mqh` was rebuilt around the documented end-backward branch method.

Low-side / positive Hook:

- same-side nodes = valleys
- branch progresses old-to-new through strictly lower valleys
- end-backward builder accepts earlier higher lows into the branch

High-side / negative Hook:

- same-side nodes = peaks
- branch progresses old-to-new through strictly higher peaks
- end-backward builder accepts earlier lower highs into the branch

### 2. Branch length

Readable branch output is capped by the documented maximum of four counted nodes.

If a candidate branch contains more than four counted nodes, it is rejected from the readable view instead of being truncated into a misleading sequence.

### 3. Minimum 1/2 validation

For branches with at least two counted nodes:

- low-side Hook requires node 2 to be strictly lower than node 1
- high-side Hook requires node 2 to be strictly higher than node 1
- an opposite-side node must exist between 1 and 2

This implements the documented minimum internal 1/2 rule.

### 4. Opposite extreme / Hook crown

The builder now stores the opposite-side extreme between branch start and branch final node:

- positive Hook crown = highest peak in the branch span
- negative Hook crown = lowest valley in the branch span

The visual renderer uses this crown for the Hook envelope curve.

### 5. Semantic minimal renderer

`FP_HookPhase02Visual.mqh` was rebuilt to avoid the earlier node-wiring failure mode.

Semantic minimal view now draws:

1. branch numbers only
2. one gray Hook envelope curve per Hook-origin context

It does not draw:

- straight sequence lines
- heavy node circles / arrows
- origin labels
- debug labels
- death / threshold / quality / type overlays

### 6. Label placement

Branch labels follow the documented side rule:

- positive / valley labels stack below the low
- negative / peak labels stack above the high

Each branch sequence has one stable color; all labels in that sequence use that color. If multiple branch labels share a node area, they are stacked outward using deterministic lanes.

## Remaining limitation

The documentation says that if branch length exceeds four nodes, `L` should be increased and the Hook context rebuilt until all branch lengths are readable. The current Phase 26 implementation rejects over-four branches from the readable view; it does not yet auto-promote to a higher `L` inside the same pass. That adaptive-L rebuild should be a separate engine-level phase.
