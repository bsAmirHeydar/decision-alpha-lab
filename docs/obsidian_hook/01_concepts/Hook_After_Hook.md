---
type: concept
title: Hook After Hook
status: canonical_draft
---
# Hook After Hook

A Hook After Hook is the valid second hook whose starting node is exactly the terminal node of the previous hook.

The last node of Hook-1 becomes the first node of Hook-2.

## Rule

> No shared terminal-start node, no valid Hook After Hook.

## Why It Matters

The shared-node rule prevents arbitrary fractal re-counting. The second hook is valid because it is structurally chained to the first hook, not because it merely looks like a hook.

## Zone Implication

A valid Hook After Hook may generate a tradable hook zone if the zone has a clear entry boundary, stop boundary, and open reward potential.
