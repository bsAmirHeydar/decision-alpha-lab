# Phase 25 — True Hook Arc and Extremum-Side Label Stacking

## Goal

Fix the remaining mismatch in the minimal Hook view:

- sequence labels should not overlap
- labels should stack **below valleys** and **above peaks**
- the Hook line should be the **Hook envelope arc**, not anything that reads like node-to-node sequence wiring

## What changed

### 1) Extremum-side label stacking

Node-number label placement now uses local point shape instead of Hook direction alone.

- valley-like nodes -> labels stack below the node
- peak-like nodes -> labels stack above the node

Collision stacking also keys by time, side, and a small price bucket, so close labels on the same swing stack more reliably.

### 2) True Hook envelope arc through the Hook crown

The old grouped curve still used a generic smooth curve that could visually resemble a connection overlay.

Now the grouped Hook curve is explicitly drawn in two halves:

- start -> crown
- crown -> end

Both halves are eased curves, and the joint passes exactly through the Hook crown.

So the visible line is the Hook envelope itself:

- start = Hook origin
- crown = Hook extreme
- end = Hook completion extreme after the crown

This matches the intended red-semicircle-style Hook drawing much more closely.
