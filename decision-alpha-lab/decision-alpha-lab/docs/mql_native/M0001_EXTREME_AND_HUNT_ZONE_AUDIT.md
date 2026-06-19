# M0001 Extreme and Live Hunt Zone Audit

## Purpose

After validating L-rule structural nodes, the next audit layer is expansion state:

```text
node -> expansion extreme -> territory / hunt zone
```

## Inputs

```text
InpShowExpansionExtremes = true
InpShowLiveHuntZones = true
InpShowInvalidatedHuntZones = false
InpMaxAuditStatesToDraw = 80
```

## Expansion extreme

For LOW nodes:

```text
extreme = highest high after active_from
```

For HIGH nodes:

```text
extreme = lowest low after active_from
```

The visual layer draws a dashed line:

```text
node price/time -> current expansion extreme price/time
```

## Live hunt zone

The live hunt zone is the current territory rectangle computed from the distance
between the node price and the tracked expansion extreme.

If the node has not been invalidated/hunted, the rectangle extends from
`active_from_time` to the current live-stream bar.

If the node is invalidated and `InpShowInvalidatedHuntZones=false`, no rectangle
is drawn for it.

## Structural node module boundary

The L-rule node detector is now exposed through:

```text
mql5/Include/DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh
```

Downstream M0001 modules should use this stable facade and avoid modifying the
validated detector internals.
