# Phase 24 — Hook Envelope Curve and Number-Only Sequences

## Goal

Fix the conceptual mismatch in the minimal Hook rendering:

- the display should **not** look like nodes being connected
- the display should show a **single Hook envelope curve** like the user's red semicircle sketch
- node sequence information should remain visible only through **stacked numbers**
- all node markers (bold filled circles/arrows) should be removable from the minimal view

## Hook envelope semantics

For each selected Hook-origin group:

- start = Hook origin
- crown = opposite-direction Hook extreme across the group's visible X-points
  - positive Hook → highest peak
  - negative Hook → lowest valley
- end = directional extreme reached **after** the crown
  - positive Hook → lowest valley after the crown
  - negative Hook → highest peak after the crown

The rendered curve is a smooth quadratic envelope through `(start, crown, end)`.

## Visual behavior

- no straight sequence lines
- no bold node markers in the minimal profile
- labels only for visible node numbers
- each sequence keeps a distinct color for its numbers
- if multiple sequence numbers land on the same node, they remain stacked vertically
