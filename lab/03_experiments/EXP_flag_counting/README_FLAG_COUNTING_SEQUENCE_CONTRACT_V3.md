# EXP_flag_counting — Sequence Contract V3 README

This experiment should use the English canonical contract files:

- `docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md`
- `docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V3.md`
- `docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md`

V3 is a logic contract, not just a visualization note.

The main change from the older attempts is that Flag Counting must not be implemented as a sliding-window four-node scanner.

The detector must behave as a sequence engine:

```text
F1 -> F2 -> F3
```

with:

- high/low-only node logic,
- raw node preservation,
- adaptive scale compression,
- F1/F2/F3-specific post-flag rules,
- ND/Hook detection at 3 or 4 compressed nodes,
- F3 terminal extension and lock behavior,
- deterministic rendering identity.

## Implementation order

Recommended implementation order:

1. RawNodeStore
2. ScaledNodeView / adaptive L compression
3. FlagBodyBuilder
4. PostFlagCorrectionAnalyzer
5. NDDetector
6. SequenceEngine
7. Renderer
8. AuditLogger
9. Anti-regression tests

Do not start with renderer patches before the detector contract is implemented. The previous chart issues were mostly caused by detector identity errors, not only label layout problems.

## Default research rendering

The default research view should show:

- candidate flags after probable flag body is hit,
- confirmed F1/F2,
- completed/extending/locked F3,
- ND labels,
- origin label `O`,
- detailed labels such as `F1 L8 Q23`,
- all lines thin and equal width.

It should hide:

- raw seeds,
- rejected candidates,
- invalidated structures,
- debug-only orphan windows.

## Critical resolved rules

- F1 invalidates at its Waist after the flag if confirmation has not happened.
- F2 invalidates at its Origin/start of Leg1, not at its Waist.
- F2 may use a waist-break branch.
- F3 is completed by its two-leg body.
- F3 locks only after the first smallest confirmed opposite F1.
- F2 starts from the deepest/farthest terminal correction after F1, not from an arbitrary internal node.
- F3 same-scale acceptance uses OR conditions:
  - Leg1 L compatibility with F2 Leg1 L within 20%, or
  - F3 flag size at least 0.70 of F2 flag size.

## What not to do

Do not draw every alternating four-node window.

Do not start F1 from the middle of an ongoing move.

Do not delete locked F3 after reversal.

Do not use candle close or candle body in F or ND logic.

Do not kill a parent sequence just because a child candidate invalidates.
