# Debug Views

## Why Debug Views Are Needed

The user wants to see all structures. But all structures must still be inspectable.

A single chart can show all emitted structures if rendering is disciplined, but debugging also needs panels and modes.

## Recommended Inputs

```text
InpDrawAllSequences = true
InpDrawRejected = false
InpDrawNDHooks = true
InpShowOnlyOpenSequenceND = false
InpShowOriginLabels = true
InpShowDetailedLevelLabels = true
InpUseSequenceColorShades = true
InpFixedLineWidth = 1
InpShowStatusPanel = true
InpShowAuditTooltips = true
InpShowLockedF3 = true
```

## View Modes

Even if default draws all structures, modes help diagnose.

```text
ALL_EMITTED
CURRENT_OPEN_CHAINS
SELECTED_CHAIN
SELECTED_F_LEVEL
ND_ONLY
AUDIT_REJECTED
```

Default:

```text
ALL_EMITTED
```

## Status Panel

Panel should not replace chart drawings. It should summarize:

```text
current chain id
active F level
status
latest F1/F2/F3
current post-flag context
number of hook branches
last invalidation/confirmation reason
```

## Audit Table

A file/CSV/log view should include transitions:

```text
time, chain, object, old_status, new_status, reason, trigger node
```

## Visual Debug Checklist

When a suspicious line appears, answer:

1. Which object id owns it?
2. Which chain owns it?
3. Is it F1/F2/F3/ND?
4. Where are Origin, Leg1, Waist, Leg2?
5. Why is it alive?
6. What would invalidate it?
7. Was it emitted by logic engine or renderer?
8. Does audit log contain its creation event?

If any answer is missing, the bug is in logical emission or audit identity, not in line drawing.

## Rejected View

Rejected objects should be hidden by default.

For debugging:

```text
InpDrawRejected = true
```

When enabled, rejected objects must be visibly different and not confused with live structures.

## ND Density Controls

Default shows all ND hooks.

Optional controls:

```text
InpShowOnlyOpenSequenceND
InpMaxNDPerChain
InpMaxNDPerViewport
InpShowBelowHalfCycleND
```

These are display filters only. They must not change logical detection.
