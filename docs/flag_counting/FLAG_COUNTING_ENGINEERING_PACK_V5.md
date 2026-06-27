# Flag Counting Engineering Pack V5

This file is the entry point for the Flag Counting Engineering Pack V5.

The V5 pack turns the latest sequence contract into an implementation-grade documentation set. It is intentionally more detailed than the previous contract files. The goal is to prevent the detector and renderer from drifting back into vague sliding-window behavior.

The pack is split into four conceptual layers plus a package index:

```text
engineering_pack_v5/
  README.md
  01_concepts/
  02_definitions/
  03_explanations/
  04_algorithms/
  05_visualization/
```

Use this document set as the source of truth before rewriting or auditing the MQL5 implementation.

## Reading Order

1. `engineering_pack_v5/README.md`
2. `01_concepts/README.md`
3. `02_definitions/README.md`
4. `03_explanations/README.md`
5. `04_algorithms/README.md`
6. `05_visualization/README.md`

## Implementation Rule

The renderer must never infer, invent, rescue, merge, or reinterpret structures. Rendering is a view of emitted logical objects only.

The detector must never treat every local alternating high/low window as an F1. Flag Counting is a chain state machine, not a pattern scanner.

## Current Status

This pack is documentation only. It intentionally does not modify code.
