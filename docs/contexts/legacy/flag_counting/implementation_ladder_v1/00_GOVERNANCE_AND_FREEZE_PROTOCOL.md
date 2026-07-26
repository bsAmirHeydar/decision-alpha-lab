# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on them.

Global non-negotiables:

- All structural decisions use candle `high` and `low` only.
- `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs.
- Equality is not a break. A level is broken only by a strict pass beyond it.
- The renderer is non-authoritative. It may only draw logical objects emitted by engines.
- Main-chart rendering and audit rendering are separate products.
- Every layer must expose enough audit fields to prove why an object exists.
- A higher layer may never silently repair a lower-layer defect.

## Level 00 — Governance and Freeze Protocol

## Canon source rule

The decision source for every Phoenix patch is:

```text
docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
```

If a ladder file, engineering-pack file, repair note, README, or legacy document conflicts with the current canon, the current canon wins. A patch that wants to change a decision must update the canon first in a governance patch.


### Problem this layer solves

Previous Phoenix iterations failed because tactical patches edited multiple semantic layers at once. Hook logic, flag-body logic, sequence ownership, renderer behavior, and label layout were changed together. When the chart broke, it was impossible to determine whether the defect came from structure detection, phase ownership, duplicate pruning, or rendering.

Level 00 prevents that by defining the engineering law of the project.

### Rule 1 — Every patch must name its layer

A patch must state its highest touched layer:

```text
L02 node patch
L04 Hook/ND patch
L07 F1 lifecycle patch
L10 sequence ownership patch
L12 renderer patch
```

A patch may touch lower-level docs/tests, but it may not casually touch unrelated upper layers.

### Rule 2 — Lower layers are frozen after acceptance

After a layer passes its acceptance tests, it becomes frozen. A later patch may only modify it if:

1. a test proves the layer is wrong;
2. the layer's document is updated;
3. the layer's regression test is updated;
4. all dependent layers are re-run.

### Rule 3 — Renderer cannot fix engine defects

If a structure is wrong, hiding it in renderer is not a fix. Renderer filters are allowed only for main-chart clarity after the audit layer has preserved the full logical output.

### Rule 4 — Hook/ND cannot starve F structures

Hook/ND is context and phase-boundary information. It may influence valid F1 root preference, but it may not become a hard gate that removes all two-leg flag structures from main chart unless the contract explicitly says so and audit proves why.

### Rule 5 — Fail-open is a diagnostic mode, not a semantic truth

Fail-open exists to prevent a visually empty chart while Hook/ND coverage is being validated. It must be labeled as fail-open in audit fields. Fail-open structures may be drawn on the main chart only if they pass flag-body and lifecycle contracts.

### Rule 6 — Audit before visual elegance

Each logical object must have an audit identity before it has a beautiful line:

- source L;
- direction;
- source engine;
- node anchors;
- price anchors;
- parent id;
- phase id;
- status;
- invalidation boundary;
- confirmation boundary;
- reason for visibility or hidden status.

### Rule 7 — Do not mix main chart and audit chart

Main chart is for canonical visible structures.

Audit chart is for raw candidates, rejected structures, duplicate losers, hidden descendants, branch counts, detailed parent ids, and engine diagnostics.

### Rule 8 — Every output must be deterministic

Given the same bars, settings, and history range, Phoenix must emit the same logical objects in the same order with the same canonical winners. Random tie-breaking is forbidden.

### Rule 9 — Commit discipline

Commit messages must include:

- canon file used;
- layer touched;
- modules touched;
- invariant preserved;
- invariant changed;
- tests run;
- known limitations.

### Rule 10 — Screenshot-driven panic patching is forbidden

A screenshot may identify symptoms but cannot be the design source. The debugging sequence is:

```text
Screenshot symptom
-> identify failed layer
-> inspect emitted audit objects
-> compare to layer contract
-> patch the layer
-> re-run lower and dependent layer tests
-> then inspect screenshot again
```

## Freeze checklist

A layer is frozen only when all are true:

- its document is complete;
- module interfaces are defined;
- audit fields exist;
- at least one golden example exists;
- edge cases are listed;
- failure symptoms are listed;
- compile passes;
- visual smoke test passes if the layer reaches renderer.

## Rollback policy

Rollback by Git alone is insufficient in MetaTrader because old chart objects and compiled `.ex5` files can survive.

Rollback protocol:

```powershell
Get-ChildItem -Recurse -Filter "FlagCountingPhoenixExperiment.ex5" | Remove-Item -Force -ErrorAction SilentlyContinue
```

Then:

```text
1. Compile the expert again.
2. Remove expert from chart.
3. Ctrl+B.
4. Delete all DAL_FCP_ objects.
5. Attach expert again.
6. Reset inputs.
```

## Forbidden patch types

- A patch that changes Hook logic and renderer label layout at the same time.
- A patch that changes F2/F3 lifecycle and duplicate pruning at the same time.
- A patch that hides structures without recording why in audit.
- A patch that introduces a new input without documenting its default and effect.
- A patch that assumes MT5 inputs reset automatically.
